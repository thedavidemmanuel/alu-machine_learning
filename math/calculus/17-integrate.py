#!/usr/bin/env python3
'''
Module for calculating the integral of a polynomial.

This module provides a function poly_integral which takes a list of coefficients
(poly) representing a polynomial and an integration constant (C), returning a
new list of coefficients representing the polynomial's integral.
'''

def poly_integral(poly, C=0):
    '''
    Calculate the integral of the given polynomial.
    
    Parameters:
    poly (list): Coefficients list where index represents power of x.
    C (int/float): Integration constant. Defaults to 0.
    
    Returns:
    list: Coefficients list representing the polynomial's integral,
          or None if input is invalid.
    '''
    if not isinstance(poly, list) or not isinstance(C, (int, float)):
        return None
    if isinstance(C, float) and C.is_integer():
        C = int(C)
    integral = [C] if C != 0 else [0]
    for power, coefficient in enumerate(poly):
        if coefficient == 0 and power == 0:
            integral = [C]
            break
        new_coefficient = coefficient / (power + 1)
        if new_coefficient.is_integer():
            new_coefficient = int(new_coefficient)
        integral.append(new_coefficient)
    if not integral[-1]:
        integral.pop()
    return integral

# Example usage:
if __name__ == "__main__":
    print(poly_integral([0]))  # Output: [0]
    print(poly_integral([5]))  # Output: [0, 5]
    print(poly_integral([6, 0, 0, 1]))  # Output: [0, 6, 0, 0, 0.25]
