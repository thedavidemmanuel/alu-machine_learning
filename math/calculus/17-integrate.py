def poly_integral(poly, C=0):
    """
    Calculate the integral of a polynomial.

    Parameters:
    poly (list): A list of coefficients, where the index represents the power of x.
    C (int): The integration constant.

    Returns:
    list: A new list of coefficients representing the integral of the polynomial.
    """
    # Check if the poly is valid
    if not all(isinstance(coef, (int, float)) for coef in poly):
        return None
    
    # Calculate the integral
    integral = [C]  # Start with the integration constant
    for power, coef in enumerate(poly):
        if coef == 0 and power == 0:
            # If the first coefficient (constant term) is zero, we can skip
            continue
        integral_coef = coef / (power + 1)
        # If integral_coef is a whole number, convert it to an integer
        integral.append(int(integral_coef) if integral_coef.is_integer() else integral_coef)
    
    return integral
