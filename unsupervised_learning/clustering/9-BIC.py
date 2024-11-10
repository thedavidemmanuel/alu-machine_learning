#!/usr/bin/env python3
"""This module contains a function that finds the best number of clusters
for a GMM using the Bayesian Information Criterion"""
import numpy as np
expectation_maximization = __import__('8-EM').expectation_maximization


def BIC(X, kmin=1, kmax=None, iterations=1000, tol=1e-5, verbose=False):
    """
    Finds the best number of clusters for a GMM using the Bayesian Information
    Criterion.

    Parameters:
        X: numpy.ndarray of shape (n, d) containing the data set
        kmin: positive integer containing the minimum number of clusters to check
        kmax: positive integer containing the maximum number of clusters to check
        iterations: positive integer containing the maximum number of iterations
        tol: non-negative float containing the tolerance for the EM algorithm
        verbose: boolean that determines if the EM algorithm should print info

    Returns:
        best_k: best value for k based on its BIC
        best_result: tuple containing pi, m, S for the best number of clusters
        l: numpy.ndarray containing the log likelihood for each cluster size
        b: numpy.ndarray containing the BIC value for each cluster size
    """
    if not isinstance(X, np.ndarray) or len(X.shape) != 2:
        return None, None, None, None

    if not isinstance(kmin, int) or kmin < 1:
        return None, None, None, None

    if kmax is not None:
        if not isinstance(kmax, int) or kmax <= kmin:
            return None, None, None, None
    else:
        kmax = X.shape[0]

    if not isinstance(iterations, int) or iterations <= 0:
        return None, None, None, None

    if not isinstance(tol, float) or tol < 0:
        return None, None, None, None

    if not isinstance(verbose, bool):
        return None, None, None, None

    n, d = X.shape
    k_range = range(kmin, kmax + 1)
    likelihoods = []
    bics = []
    results = []

    best_bic = float('inf')
    best_k = None
    best_result = None

    for k in k_range:
        # Calculate number of parameters
        # pi: k-1 (sum to 1 constraint)
        # means: k*d
        # covariances: k*d*d (symmetric matrices)
        n_params = (k - 1) + (k * d) + (k * d * (d + 1) // 2)

        # Run EM algorithm
        pi, m, S, _, ll = expectation_maximization(
            X, k, iterations, tol, verbose)

        if pi is None or m is None or S is None:
            continue

        # Calculate BIC
        bic = n_params * np.log(n) - 2 * ll
        
        likelihoods.append(ll)
        bics.append(bic)
        results.append((pi, m, S))

        # Update best result if this BIC is lower
        if bic < best_bic:
            best_bic = bic
            best_k = k
            best_result = (pi, m, S)

    if not likelihoods:  # If no valid results were found
        return None, None, None, None

    return (best_k,
            best_result,
            np.array(likelihoods),
            np.array(bics))
