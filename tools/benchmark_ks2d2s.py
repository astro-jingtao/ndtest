"""Measure the running time of the two-dimensional Kolmogorov-Smirnov test.

Two samples of `--n` standard normal points are drawn. Sample 1 has independent
coordinates and sample 2 has y = x + noise. The script times one evaluation of
the statistic in one direction and one call of `ks2d2s` with its analytic p-value.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
import statistics
import time

import numpy as np

from ndtest.ksnd import ks2d2s, maxdist_wraper


def samples(n: int, seed: int) -> tuple[np.ndarray, ...]:
    """Return x1, y1, x2, y2 of the two samples."""
    rng = np.random.default_rng(seed)
    x1, y1 = rng.normal(0, 1, n), rng.normal(0, 1, n)
    x2 = rng.normal(0, 1, n)
    y2 = x2 + rng.normal(0, 1, n)
    return x1, y1, x2, y2


def per_call_ms(
    func: Callable[[], object], repeats: int, min_batch: float = 0.1
) -> tuple[float, float]:
    """Return the smallest and the median time of one call, in milliseconds.

    A batch holds as many calls as take about `min_batch` seconds.
    """
    func()
    start = time.perf_counter()
    func()
    number = max(1, int(min_batch / (time.perf_counter() - start)))
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        for _ in range(number):
            func()
        times.append((time.perf_counter() - start) / number * 1000)
    return min(times), statistics.median(times)


def main() -> None:
    """Run the timing for the requested sample size."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=10_000, help="points per sample")
    parser.add_argument("--repeats", type=int, default=7, help="timed batches per measurement")
    parser.add_argument("--seed", type=int, default=0, help="seed of the sample generation")
    args = parser.parse_args()

    x1, y1, x2, y2 = samples(args.n, args.seed)

    def one_direction() -> None:
        maxdist_wraper(x1, y1, x2, y2)

    def test() -> None:
        ks2d2s(x1, y1, x2, y2)

    for label, func in (("one direction", one_direction), ("ks2d2s", test)):
        smallest, median = per_call_ms(func, args.repeats)
        print(f"{label:14s} n={args.n}: min {smallest:.2f} ms, median {median:.2f} ms")


if __name__ == "__main__":
    main()
