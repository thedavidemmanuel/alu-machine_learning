#!/usr/bin/env python3
"""Slice Me Up script"""

arr = [9, 8, 2, 3, 9, 4, 1, 0, 3]
arr1 = arr[:2]  # the first two numbers of arr
arr2 = arr[-5:]  # the last five numbers of arr
arr3 = arr[1:6]  # the 2nd through 6th numbers of arr

print("The first two numbers of the array are: {}".format(arr1))
print("The last five numbers of the array are: {}".format(arr2))
print("The 2nd through 6th numbers of the array are: {}".format(arr3))
