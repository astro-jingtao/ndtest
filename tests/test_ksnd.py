"""Tests of the two-dimensional two-sample Kolmogorov-Smirnov test."""

import numpy as np
import pytest

from ndtest.ksnd import avgmaxdist, ks2d2s, maxdist_wraper


def sample(rng, n, center=(0.0, 0.0)):
    """Draw one sample whose x coordinates stay distinct in single precision."""
    x = center[0] + rng.permutation(n) + rng.uniform(0.05, 0.95, size=n)
    y = center[1] + rng.normal(size=n)
    return x, y


def reference_maxdist(x1, y1, x2, y2):
    """Largest difference between the two empirical distribution functions.

    At every point of the first sample, the plane is cut into the four
    quadrants and the fractions of both samples in each quadrant are compared.
    This is the definition of the statistic, evaluated in double precision and
    without any sorting, so it is slow and independent of the Fortran kernel.
    """
    n1 = len(x1)
    largest = 0.0
    for i in range(n1):
        left, below = x1 <= x1[i], y1 <= y1[i]
        far_left, far_below = x2 <= x1[i], y2 <= y1[i]
        first = (left & below, left & ~below, ~left & below, ~left & ~below)
        second = (
            far_left & far_below,
            far_left & ~far_below,
            ~far_left & far_below,
            ~far_left & ~far_below,
        )
        a1, b1, c1, d1 = (np.mean(part) for part in first)
        a2, b2, c2, d2 = (np.mean(part) for part in second)
        difference = np.array((a1 - a2 - 1 / n1, b1 - b2, c1 - c2, d1 - d2))
        largest = max(largest, difference.max() + 1 / n1, -difference.min())
    return largest


@pytest.fixture
def two_samples():
    rng = np.random.default_rng(0)
    return sample(rng, 300), sample(rng, 350)


@pytest.fixture
def seeded_bootstrap():
    """Make the bootstrap resamples repeatable for the duration of a test."""
    state = np.random.get_state()
    np.random.seed(0)
    yield
    np.random.set_state(state)


class TestDocumentedUsage:
    def test_readme_example(self):
        rng = np.random.default_rng(0)
        x1, y1 = rng.normal(size=(2, 1000))
        x2, y2 = rng.normal(size=(2, 1000))
        d, p = ks2d2s(x1, y1, x2, y2)
        assert 0 <= d <= 1
        assert 0 <= p <= 1
        d_boot, p_boot = ks2d2s(x1, y1, x2, y2, nboot=200, n_jobs=2)
        assert 0 <= d_boot <= 1
        assert 0 <= p_boot <= 1


class TestStatistic:
    def test_identical_samples_give_one_over_n(self):
        rng = np.random.default_rng(1)
        x, y = sample(rng, 400)
        d, _ = ks2d2s(x, y, x, y)
        assert d == pytest.approx(1 / 400, rel=1e-5)

    def test_separated_samples_give_the_largest_possible_difference(self):
        rng = np.random.default_rng(2)
        x1, y1 = sample(rng, 200)
        x2, y2 = sample(rng, 300, center=(1000.0, 50.0))
        assert maxdist_wraper(x1, y1, x2, y2) == 1.0
        d, _ = ks2d2s(x1, y1, x2, y2)
        assert d > 0.9

    def test_shift_increases_statistic(self, two_samples):
        (x1, y1), (x2, y2) = two_samples
        d_same, _ = ks2d2s(x1, y1, x1, y1)
        d_independent, _ = ks2d2s(x1, y1, x2, y2)
        d_shifted, _ = ks2d2s(x1, y1, x2, y2 + 0.5)
        assert d_same < d_independent < d_shifted

    def test_agrees_with_reference(self, two_samples):
        (x1, y1), (x2, y2) = two_samples
        assert maxdist_wraper(x1, y1, x2, y2) == pytest.approx(
            reference_maxdist(x1, y1, x2, y2), rel=1e-5, abs=1e-6
        )
        assert maxdist_wraper(x2, y2, x1, y1) == pytest.approx(
            reference_maxdist(x2, y2, x1, y1), rel=1e-5, abs=1e-6
        )
        expected = (reference_maxdist(x1, y1, x2, y2) + reference_maxdist(x2, y2, x1, y1)) / 2
        assert avgmaxdist(x1, y1, x2, y2) == pytest.approx(expected, rel=1e-5, abs=1e-6)

    def test_average_does_not_depend_on_sample_order(self, two_samples):
        (x1, y1), (x2, y2) = two_samples
        assert avgmaxdist(x1, y1, x2, y2) == avgmaxdist(x2, y2, x1, y1)

    def test_tied_x_coordinates_give_a_statistic_within_the_bounds(self):
        rng = np.random.default_rng(7)
        x1 = rng.integers(0, 5, size=30).astype(float)
        y1 = rng.integers(0, 5, size=30).astype(float)
        x2 = rng.integers(0, 5, size=40).astype(float)
        y2 = rng.integers(0, 5, size=40).astype(float)
        assert 0 <= maxdist_wraper(x1, y1, x2, y2) <= 1
        assert 0 <= maxdist_wraper(x2, y2, x1, y1) <= 1


class TestPValue:
    def test_identical_samples_are_not_rejected(self):
        rng = np.random.default_rng(3)
        x, y = sample(rng, 400)
        _, p = ks2d2s(x, y, x, y)
        assert p > 0.99

    def test_separated_samples_are_rejected(self):
        rng = np.random.default_rng(4)
        x1, y1 = sample(rng, 200)
        x2, y2 = sample(rng, 300, center=(1000.0, 50.0))
        _, p = ks2d2s(x1, y1, x2, y2)
        assert p < 1e-10

    def test_shift_lowers_p_value(self, two_samples):
        (x1, y1), (x2, y2) = two_samples
        _, p_independent = ks2d2s(x1, y1, x2, y2)
        _, p_shifted = ks2d2s(x1, y1, x2, y2 + 0.5)
        assert p_shifted < p_independent

    def test_bootstrap_p_value_is_a_fraction_of_resamples(self, two_samples):
        (x1, y1), (x2, y2) = two_samples
        nboot = 100
        _, p = ks2d2s(x1, y1, x2, y2, nboot=nboot)
        assert 0 <= p <= 1
        assert p * nboot == pytest.approx(round(p * nboot))

    def test_bootstrap_identical_samples_are_not_rejected(self):
        rng = np.random.default_rng(5)
        x, y = sample(rng, 300)
        _, p = ks2d2s(x, y, x, y, nboot=100)
        assert p == 1.0

    def test_bootstrap_shift_is_rejected(self, two_samples):
        (x1, y1), (x2, y2) = two_samples
        _, p = ks2d2s(x1, y1, x2, y2 + 1.0, nboot=100)
        assert p < 0.5

    def test_bootstrap_p_value_does_not_depend_on_n_jobs(self, two_samples, seeded_bootstrap):
        (x1, y1), (x2, y2) = two_samples
        _, p_serial = ks2d2s(x1, y1, x2, y2, nboot=50, n_jobs=1)
        np.random.seed(0)
        _, p_parallel = ks2d2s(x1, y1, x2, y2, nboot=50, n_jobs=2)
        assert p_serial == p_parallel


class TestInputs:
    def test_lists_are_accepted(self):
        d, _ = ks2d2s([1, 2], [1, 2], [1, 2], [1, 2])
        assert d == pytest.approx(0.5)

    def test_mismatched_lengths_raise(self):
        with pytest.raises(AssertionError):
            ks2d2s([1, 2], [1, 2, 3], [1, 2], [1, 2])


class TestExactValues:
    """Exact single-precision values of the statistic for fixed inputs.

    The kernel counts in integers and divides once, so its result is the same
    float32 on every platform as long as the x coordinates of the first sample
    have no ties: with such ties the count follows the order of tied elements,
    which the default `numpy.argsort` does not keep.
    """

    def test_continuous_samples(self, two_samples):
        (x1, y1), (x2, y2) = two_samples
        assert maxdist_wraper(x1, y1, x2, y2) == np.float32(0.14809525)
        assert maxdist_wraper(x2, y2, x1, y1) == np.float32(0.14761907)

    def test_tied_y_and_tied_x_of_the_second_sample(self):
        rng = np.random.default_rng(7)
        x1 = rng.permutation(30) + rng.uniform(0.05, 0.95, size=30)
        y1 = rng.integers(0, 5, size=30).astype(float)
        x2 = rng.integers(0, 5, size=40).astype(float) + rng.choice([0.0, 0.5])
        y2 = rng.integers(0, 5, size=40).astype(float)
        assert maxdist_wraper(x1, y1, x2, y2) == np.float32(0.83333337)

    def test_coordinates_beyond_single_precision_resolution(self):
        rng = np.random.default_rng(11)
        x1 = 1e6 + rng.normal(size=120) * 1e-3
        y1 = 1e6 + rng.normal(size=120) * 1e-3
        x2 = 1e6 + rng.normal(size=90) * 1e-3
        y2 = 1e6 + rng.normal(size=90) * 1e-3
        assert maxdist_wraper(x1, y1, x2, y2) == np.float32(1.0)
        assert maxdist_wraper(x2, y2, x1, y1) == np.float32(1.0)
