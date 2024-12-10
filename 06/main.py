# Task 1
from random import sample


def example():
    pass

# Task 2
def example2():
    print("I am an example function")

def print_triangle(height):
    for i in range(1, height + 1):
        spaces = ' ' * (height - i)
        stars = '*' * (2 * i - 1)
        print(spaces + stars)

def add(a: int, b: int) -> int:
    return a + b


def recursion(n):
    if n == 0:
        return
    recursion(n - 1)
    print(n)


def main():
    print("How are you today?", __name__)
    example2()
    print_triangle(5)
    print(f'{3} + {4} = {add(3, 4)}')
    recursion(5)


if __name__ == "__main__":
    main()





