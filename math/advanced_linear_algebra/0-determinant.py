#!/usr/bin/env python3
"""
A module to calculate the determinant of a matrix.

Functions:
    determinant(matrix): Calculates the determinant of a matrix.
"""


def determinant(matrix):
    """
    Calculates the determinant of a matrix.

    Args:
        matrix (list of lists): The matrix to calculate the determinant for.

    Returns:
        int or float: The determinant of the matrix.

    Raises:
        TypeError: If the matrix is not a list of lists.
        ValueError: If the matrix is not square.
    """
    # Validate the matrix is a list of lists
    if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise TypeError("matrix must be a list of lists")

    # Validate the matrix is square
    num_rows = len(matrix)
    for row in matrix:
        if len(row) != num_rows:
            raise ValueError("matrix must be a square matrix")

    # Base case: 0x0 matrix has determinant 1
    if num_rows == 0:
        return 1

    # Base case: 1x1 matrix has determinant equal to its element
    if num_rows == 1:
        return matrix[0][0]

    # Calculate the determinant for matrices larger than 1x1
    det = 0
    for col in range(num_rows):
        minor = [row[:col] + row[col + 1:] for row in matrix[1:]]
        det += (-1) ** col * matrix[0][col] * determinant(minor)

    return det
