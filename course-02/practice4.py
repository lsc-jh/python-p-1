import math
from math import log

def recursion(n):
    if n >= 0:
        return n + recursion(n - 1)
    else:
        return 0




# print(recursion(5))

def hello(list):
    for i in list:
        print(f"Hello {i}", end=" ")


hello([3, 4, 5, 6, "Leo", 4 * 2])

x = 11
y = 4

x = x % y
x = x % y
y = y % x

print(y)