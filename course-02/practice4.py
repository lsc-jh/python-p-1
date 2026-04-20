def recursion(n):
    if n >= 0:
        return n + recursion(n - 1)
    else:
        return 0


print(recursion(5))
