# original version from https://github.com/syrte/ndtest
"""Two-dimensional two-sample Kolmogorov-Smirnov test with a Fortran kernel."""

from __future__ import annotations

from joblib import Parallel, delayed
import numpy as np
from numpy.typing import ArrayLike
from scipy.stats import kstwobign

from ndtest.maxdist import maxdist

__all__ = ["ks2d2s"]


def ks2d2s(
    x1: ArrayLike,
    y1: ArrayLike,
    x2: ArrayLike,
    y2: ArrayLike,
    *,
    nboot: int | None = None,
    n_jobs: int = 1,
    rng: np.random.Generator | int | None = None,
    backend: str | None = "threading",
) -> tuple[np.floating, np.floating]:
    """Two-dimensional Kolmogorov-Smirnov test on two samples.
    Parameters
    ----------
    x1, y1 : array_like, shape (n1,)
        Data of sample 1.
    x2, y2 : array_like, shape (n2,)
        Data of sample 2. The two samples may have different sizes.
    nboot : None or int
        Number of bootstrap resamples that estimate the p-value; a large number is expected.
        If None, an analytic approximation of the p-value is used.
    n_jobs : int, optional
        The number of jobs used for the bootstrap p-value. If -1, all CPUs are used.
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator for the bootstrap resamples. When `rng` is None, a new `numpy.random.Generator` is created using entropy from the operating system. Types other than `numpy.random.Generator` are passed to `numpy.random.default_rng` to instantiate a `Generator`.
    backend : str, optional
        The joblib backend that runs the bootstrap resamples when `n_jobs` is not 1. The default `"threading"` runs them in threads of the calling process, which start no worker processes; the Fortran kernel and the sorting release the GIL, so the threads run at the same time. None leaves the choice to joblib, so a `joblib.parallel_backend` context of the caller applies.

    Returns
    -------
    D : float
        KS statistic.
    p : float
        Two-tailed p-value.

    Notes
    -----
    This is the two-sided K-S test. Small p-values mean that the two samples are significantly different.
    With `nboot=None` the p-value is an approximation, as the analytic distribution of the statistic is unknown. The approximation
    is accurate enough when N > ~20 and p-value < ~0.20 or so. When p-value > 0.20, the value may not be accurate,
    but it certainly implies that the two samples are not significantly different. (cf. Press 2007)

    References
    ----------
    Peacock, J.A. 1983, Two-Dimensional Goodness-of-Fit Testing in Astronomy, MNRAS, 202, 615-627
    Fasano, G. and Franceschini, A. 1987, A Multidimensional Version of the Kolmogorov-Smirnov Test, MNRAS, 225, 155-170
    Press, W.H. et al. 2007, Numerical Recipes, section 14.8

    """
    x1 = np.asarray(x1)
    y1 = np.asarray(y1)
    x2 = np.asarray(x2)
    y2 = np.asarray(y2)

    assert len(x1) == len(y1)
    assert len(x2) == len(y2)
    n1, n2 = len(x1), len(x2)
    D = avgmaxdist(x1, y1, x2, y2)

    if nboot is None:
        sqen = np.sqrt(n1 * n2 / (n1 + n2))
        r1 = np.corrcoef(x1, y1)[0, 1]
        r2 = np.corrcoef(x2, y2)[0, 1]
        r = np.sqrt(1 - 0.5 * (r1**2 + r2**2))
        d = D * sqen / (1 + r * (0.25 - 0.75 / sqen))
        p = kstwobign.sf(d)
    else:
        rng = np.random.default_rng(rng)
        n = n1 + n2
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])

        ix1_ix2_lst = []

        for _ in range(nboot):
            idx = rng.choice(n, n, replace=True)
            ix1_ix2_lst.append((idx[:n1], idx[n1:]))

        with Parallel(n_jobs=n_jobs, backend=backend) as parallel:
            d = parallel(
                delayed(avgmaxdist)(x[ix1], y[ix1], x[ix2], y[ix2]) for ix1, ix2 in ix1_ix2_lst
            )

        p = np.mean(np.asarray(d) > D)

    return D, p


def avgmaxdist(x1: np.ndarray, y1: np.ndarray, x2: np.ndarray, y2: np.ndarray) -> np.floating:
    D1 = maxdist_wrapper(x1, y1, x2, y2)
    D2 = maxdist_wrapper(x2, y2, x1, y1)
    return (D1 + D2) / 2


def maxdist_wrapper(x1: np.ndarray, y1: np.ndarray, x2: np.ndarray, y2: np.ndarray) -> np.floating:
    # The kernel counts a group of equal x coordinates as a whole, so the order of tied points,
    # which differs between sort algorithms and CPUs, does not reach the statistic.
    order1, order2 = np.argsort(x1), np.argsort(x2)
    # The dense ranks of the y coordinates over both samples: two coordinates are equal exactly
    # when they have the same rank.
    rank = dense_rank(np.concatenate([y1, y2]))
    rank1, rank2 = rank[: len(x1)], rank[len(x1) :]
    D_max = np.zeros(1, dtype=np.float64)
    maxdist(x1[order1], rank1[order1] + 1, x2[order2], rank2[order2] + 1, D_max)
    return D_max[0]


def dense_rank(values: np.ndarray) -> np.ndarray:
    """Dense rank of each value among the distinct values: 0 for the smallest, equal values share a rank."""
    order = np.argsort(values)
    sorted_values = values[order]
    # new_value[i] is True where the i-th smallest value differs from the one before it
    new_value = np.empty(len(values), dtype=bool)
    new_value[0] = True
    new_value[1:] = sorted_values[1:] != sorted_values[:-1]
    rank = np.empty(len(values), dtype=np.int32)
    rank[order] = np.cumsum(new_value, dtype=np.int32) - 1
    return rank
