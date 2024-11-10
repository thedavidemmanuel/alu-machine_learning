#!/usr/bin/env python3
"""This module contains a function that finds the best number of clusters
for a GMM using the Bayesian Information Criterion"""
import numpy as np
expectation_maximization = __import__('8-EM').expectation_maximization


def BIC(X, kmin=1, kmax=None, iterations=1000, tol=1e-5, verbose=False):
    """
    Finds the best number of clusters for a GMM using BIC.

    Args:
        X: numpy.ndarray of shape (n, d) containing the data set
        kmin: minimum number of clusters to check for (inclusive)
        kmax: maximum number of clusters to check for (inclusive)
        iterations: maximum number of iterations for the EM algorithm
        tol: tolerance for the EM algorithm
        verbose: determines if EM algorithm should print information

    Returns:
        best_k: best value for k based on its BIC
        best_result: tuple containing pi, m, S
        l: numpy.ndarray with log likelihood for each cluster size
        b: numpy.ndarray with BIC value for each cluster size
    """
    if not isinstance(X, np.ndarray) or len(X.shape) != 2:
        return None, None, None, None

    if not isinstance(kmin, int) or kmin < 1:
        return None, None, None, None

    n, d = X.shape
    if kmax is None:
        kmax = n
    elif not isinstance(kmax, int) or kmax <= kmin:
        return None, None, None, None

    if not isinstance(iterations, int) or iterations <= 0:
        return None, None, None, None

    if not isinstance(tol, float) or tol < 0:
        return None, None, None, None

    if not isinstance(verbose, bool):
        return None, None, None, None

    best_k = 0
    best_result = None
    best_bic = float('inf')
    l = np.zeros(kmax - kmin + 1)
    b = np.zeros(kmax - kmin + 1)

    k = kmin
    i = 0
    while k <= kmax:
        # Run EM for current k
        pi, m, S, _, ll = expectation_maximization(X, k, iterations, tol, verbose)
        
        if pi is None:
            return None, None, None, None
            
        # Calculate BIC
        p = (k - 1) + (k * d) + (k * d * (d + 1) // 2)
        bic = p * np.log(n) - 2 * ll
        
        # Store results
        l[i] = ll
        b[i] = bic
        
        # Update best if needed
        if bic < best_bic:
            best_k = k
            best_result = (pi, m, S)
            best_bic = bic
            
        k += 1
        i += 1

    if best_k == 0:
        return None, None, None, None

    return best_k, best_result, l, b
