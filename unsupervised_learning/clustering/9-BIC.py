#!/usr/bin/env python3
"""Function that finds the best number of clusters for a GMM using BIC"""
import numpy as np
expectation_maximization = __import__('8-EM').expectation_maximization


def BIC(X, kmin=1, kmax=None, iterations=1000, tol=1e-5, verbose=False):
    """
    Find best number of clusters for GMM using Bayesian Information Criterion.

    Args:
        X: numpy.ndarray (n, d) containing data set
        kmin: minimum number of clusters to check (inclusive)
        kmax: maximum number of clusters to check (inclusive)
        iterations: maximum number of iterations for EM
        tol: tolerance for EM algorithm
        verbose: boolean for verbosity

    Returns:
        best_k: best value for k based on BIC
        best_result: tuple containing (pi, m, S) for best k
        l: numpy.ndarray with log likelihood for each k
        b: numpy.ndarray with BIC value for each k
    """
    # Input validation
    if not isinstance(X, np.ndarray) or len(X.shape) != 2:
        return None, None, None, None
    if not isinstance(kmin, int) or kmin < 1:
        return None, None, None, None
    if not isinstance(iterations, int) or iterations <= 0:
        return None, None, None, None
    if not isinstance(tol, float) or tol < 0:
        return None, None, None, None
    if not isinstance(verbose, bool):
        return None, None, None, None

    n, d = X.shape
    if kmax is None:
        kmax = 10
    if not isinstance(kmax, int) or kmax <= kmin:
        return None, None, None, None

    # Initialize arrays for storing results
    size = kmax - kmin + 1
    l = np.zeros(size)
    b = np.zeros(size)
    results = [(None, None, None)] * size
    k = kmin
    idx = 0

    # Single loop through all k values
    while k <= kmax:
        # Run EM algorithm
        pi, m, S, _, ll = expectation_maximization(X, k, iterations, tol, verbose)

        if pi is None:
            return None, None, None, None

        # Calculate BIC
        p = (k - 1) + (k * d) + (k * d * (d + 1) // 2)
        bic = p * np.log(n) - 2 * ll

        # Store results
        l[idx] = ll
        b[idx] = bic
        results[idx] = (pi, m, S)

        k += 1
        idx += 1

    # Find best k based on minimum BIC
    best_idx = np.argmin(b)
    best_k = kmin + best_idx

    return best_k, results[best_idx], l, b
