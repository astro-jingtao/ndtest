# original version from https://github.com/syrte/ndtest
# 209 ms for 10000 + 10000 points

from __future__ import division

import numpy as np
from joblib import Parallel, delayed
from numpy import random
from scipy.stats import kstwobign, pearsonr

from .maxdist import maxdist

__all__ = ['ks2d2s']


def ks2d2s(x1, y1, x2, y2, nboot=None, n_jobs=1):
    '''Two-dimensional Kolmogorov-Smirnov test on two samples. 
    Parameters
    ----------
    x1, y1 : ndarray, shape (n1, )
        Data of sample 1.
    x2, y2 : ndarray, shape (n2, )
        Data of sample 2. Size of two samples can be different.
    nboot : None or int
        Number of bootstrap resample to estimate the p-value. A large number is expected.
        If None, an approximate analytic estimate will be used.
    n_jobs : int, optional
        The number of jobs to use for the bootstrap resampling based p-value estimation. If -1, all CPUs are used.

    Returns
    -------
    D : float, optional
        KS statistic.
    p : float
        Two-tailed p-value.
    

    Notes
    -----
    This is the two-sided K-S test. Small p-values means that the two samples are significantly different. 
    Note that the p-value is only an approximation as the analytic distribution is unkonwn. The approximation
    is accurate enough when N > ~20 and p-value < ~0.20 or so. When p-value > 0.20, the value may not be accurate,
    but it certainly implies that the two samples are not significantly different. (cf. Press 2007)

    References
    ----------
    Peacock, J.A. 1983, Two-Dimensional Goodness-of-Fit Testing in Astronomy, MNRAS, 202, 615-627
    Fasano, G. and Franceschini, A. 1987, A Multidimensional Version of the Kolmogorov-Smirnov Test, MNRAS, 225, 155-170
    Press, W.H. et al. 2007, Numerical Recipes, section 14.8

    '''
    x1 = np.asarray(x1)
    y1 = np.asarray(y1)
    x2 = np.asarray(x2)
    y2 = np.asarray(y2)

    assert (len(x1) == len(y1)) and (len(x2) == len(y2))
    n1, n2 = len(x1), len(x2)
    D = avgmaxdist(x1, y1, x2, y2)

    if nboot is None:
        sqen = np.sqrt(n1 * n2 / (n1 + n2))
        r1 = pearsonr(x1, y1)[0]
        r2 = pearsonr(x2, y2)[0]
        r = np.sqrt(1 - 0.5 * (r1**2 + r2**2))
        d = D * sqen / (1 + r * (0.25 - 0.75 / sqen))
        p = kstwobign.sf(d)
    else:
        n = n1 + n2
        x = np.concatenate([x1, x2])
        y = np.concatenate([y1, y2])

        ix1_ix2_lst = []

        for _ in range(nboot):
            idx = random.choice(n, n, replace=True)
            ix1_ix2_lst.append((idx[:n1], idx[n1:]))

        with Parallel(n_jobs=n_jobs) as parallel:
            d = parallel(
                delayed(avgmaxdist)(x[ix1], y[ix1], x[ix2], y[ix2])
                for ix1, ix2 in ix1_ix2_lst)

        p = np.sum(d > D).astype('f') / nboot

    return D, p


def avgmaxdist(x1, y1, x2, y2):
    D1 = maxdist_wraper(x1, y1, x2, y2)
    D2 = maxdist_wraper(x2, y2, x1, y1)
    return (D1 + D2) / 2


def maxdist_wraper(x1, y1, x2, y2):
    sort1 = np.argsort(x1)
    sort2 = np.argsort(x2)
    D_max = np.zeros(1, dtype=np.float32)
    maxdist(x1, y1, sort1 + 1, x2, y2, sort2 + 1, D_max)
    return D_max[0]
