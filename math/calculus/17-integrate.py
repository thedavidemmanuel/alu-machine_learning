#!/usr/bin/env python3

def poly_integral(poly, C=0):
    '''
    Calculates the integral of the given polynomial.

    Parameters:
    poly (list): A list of coefficients, where the index represents the power of x.
    C (int or float): The integration constant.

    Returns:
    list: A new list of coefficients representing the integral of the polynomial.
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
        if coefficient % (power + 1) == 0:
            new_coefficient = coefficient // (power + 1)
        else:
            new_coefficient = coefficient / (power + 1)
        integral.append(new_coefficient)
    while integral[-1] == 0 and len(integral) > 1:
        integral.pop()
    return integral

# Example usage:
poly = [5, 3, 0, 1]  # Represents the polynomial 5 + 3x + x^3
integral = poly_integral(poly)
print(integral)  # Output should be [0, 5, 1.5, 0, 0.25]
