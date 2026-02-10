def add(a, b):
    return a + b


def is_even(n):
    return n % 2 == 0


def clamp(number, min, max):
    if number < min:
        return min

    if number > max:
        return max

    return number


def squares(numbers):
    out = []
    for number in numbers:
        out.append(number ** 2)
    return out


print("add(3, 4):", add(3, 4))
print("is_even(5):", is_even(5))
print("is_even(6):", is_even(6))
print("clamp(2, 4, 6):", clamp(2, 4, 6))
print("squares([]):", squares([]))
print("squares([1, 2, 3]):", squares([1, 2, 3]))


# Error handling

def safe_int(n):
    try:
        return int(n)
    except ValueError:
        print(f"Man, are you sure '{n}' is a number?")
        return None


def safe_div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 0


print("safe_int('5'):", safe_int('5'))
print("safe_int('0'):", safe_int('0'))
print("safe_int('leo'):", safe_int('leo'))
print("safe_div(1, 0):", safe_div(1, 0))


def improved_squares(numbers):
    out = []
    for number in numbers:
        try:
            out.append(number ** 2)
        except TypeError:
            print(f"Sadly, {number} is not a number.")
    return out


print(improved_squares([1, 2, 3]))
print(improved_squares([1, "2", 3]))
