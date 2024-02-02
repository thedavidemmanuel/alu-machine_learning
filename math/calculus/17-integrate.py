#!/usr/bin/env python3
'''
Module for calculating the integral of a polynomial.

This module provides a function poly_integral which takes a list of coefficients
(poly) representing a polynomial and an integration constant (C), returning a
new list of coefficients representing the polynomial's integral.
'''


def poly_integral(poly, C=0):
    '''
    Calculates the integral of the given polynomial.

    The index represents the power of x, and the value at that index
    represents the coefficient.

    Parameters:
    poly (list): Coefficients list where index represents power of x.
    C (int/float): Integration constant. Defaults to 0.

    Returns:
    list: Coefficients list representing the polynomial's integral,
          or None if input is invalid.
    '''
    if not isinstance(poly, list) or not poly or not isinstance(C, (int, float)):
        return None
    if isinstance(C, float) and C.is_integer():
        C = int(C)
    integral = [C] if C != 0 else []
    for power, coefficient in enumerate(poly):
        if power == 0 and coefficient == 0:
            continue
        new_coefficient = coefficient / (power + 1)
        if new_coefficient.is_integer():
            new_coefficient = int(new_coefficient)
        integral.append(new_coefficient)
    while len(integral) > 1 and integral[-1] == 0:
        integral.pop()
    return integral


# Example usage:
if __name__ == "__main__":
    # Add any relevant example calls to the function here for testing
    pass
