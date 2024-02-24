#!/usr/bin/env python3
"""
This module defines a function that calculates the definiteness of a matrix.
"""
import numpy as np

def definiteness(matrix):
    """
    Calculates the definiteness of a matrix.

    Args:
    matrix (numpy.ndarray): The matrix whose definiteness should be calculated.

    Returns:
    str: Description of matrix definiteness, or None if conditions aren't met.
    """
    if not isinstance(matrix, np.ndarray):
        return "matrix is not a numpy.ndarray"
    if matrix.size == 0 or matrix.shape[0] != matrix.shape[1]:
        return None
    if not np.allclose(matrix, matrix.T):
        return "matrix is not symmetric"

    eigenvalues = np.linalg.eigvals(matrix)
    all_positive = np.all(eigenvalues > 0)
    all_nonnegative = np.all(eigenvalues >= 0)
    all_negative = np.all(eigenvalues < 0)
    all_nonpositive = np.all(eigenvalues <= 0)

    if all_positive:
        return "matrix is positive definite"
    if all_nonnegative and not all_positive:
        return "matrix is positive semi-definite"
    if all_negative:
        return "matrix is negative definite"
    if all_nonpositive and not all_negative:
        return "matrix is negative semi-definite"
    if np.any(eigenvalues > 0) and np.any(eigenvalues < 0):
        return "matrix is indefinite"
    return None
