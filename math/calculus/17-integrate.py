#!/usr/bin/env python3
'''
Module for calculating the integral of a polynomial.

This module provides a function poly_integral which takes a list of coefficients
(poly) representing a polynomial and an integration constant (C) and returns a
new list of coefficients representing the integral of the polynomial.
'''

def poly_integral(poly, C=0):
    '''
    Calculates the integral of the given polynomial.

    The index of the list represents the power of x, and the value at that index
    represents the coefficient.

    Parameters:
    poly (list): A list of coefficients, where the index represents the power of x.
    C (int or float): The integration constant. Defaults to 0.

    Returns:
    list: A new list of coefficients representing the integral of the polynomial,
          or None if input is invalid.
    '''
    if not isinstance(poly, list) or not poly:
        return None
    if not isinstance(C, (int, float)):
        return None
    for coefficient in poly:
        if not isinstance(coefficient, (int, float)):
            return None
    if isinstance(C, float) and C.is_integer():
        C = int(C)
    integral = [C]
    for power, coefficient in enumerate(poly):
        if power == 0 and coefficient == 0:
            continue
        if coefficient % (power + 1) == 0:
            new_coefficient = coefficient // (power + 1)
        else:
            new_coefficient = coefficient / (power + 1)
        integral.append(new_coefficient)
    while integral[-1] == 0 and len(integral) > 1:
        integral.pop()
    return integral

# Remember to add the correct module-level docstring at the top of the file.
