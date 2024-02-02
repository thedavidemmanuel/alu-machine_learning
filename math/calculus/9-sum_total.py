#!/usr/bin/env python3
'''
Module for calculating the summation of i squared from 1 to n.
'''

def summation_i_squared(n):
    '''
    Calculate the sum of the squares of all integers from 1 to n.

    Parameters:
    n (int): The stopping condition.

    Returns:
    int: The integer value of the sum.
    '''
    if not isinstance(n, int) or n < 1:
        return None
    return (n * (n + 1) * (2 * n + 1)) // 6

# Example usage:
if __name__ == "__main__":
    n = 5
    print(summation_i_squared(n))  # Expected output is 55
