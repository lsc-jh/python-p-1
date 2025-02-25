
def recursion(n):
    if n == 0:
        return
    print(n)
    recursion(n - 1)
    print(n)

# 5! = 1 * 2 * 3 * 4 * 5

# 5! = 5 * 4 * 3 * 2 * 1

def factorial(n):
    if n == 1:
        return 1
    n1 = factorial(n - 1)
    result = n1 * n
    return result


def factorial2(n):
    if n == 1:
        return 1

    return n * factorial2(n - 1)

def main():
    # recursion(5)
    fact = factorial(5)
    print(fact)

if __name__ == '__main__':
    main()