"""
This is a practice class, where we try out multiple aspects of Python.
I'm enjoying this class very much!!
"""

# This is a single comment

print("Hello there!")

language = "Python"
# You can import anywhere
from datetime import datetime
year = datetime.now().year
print(year, language)
print("I'm learning", language, "in", year, ".")

big_text = """Hi, I'm Jim!
Nice to meet you!
"""
print(big_text)

dummy_text = "  Hello world!  \n"
stripped_dummy_text = dummy_text.strip()

print(dummy_text)
print("raw:", repr(dummy_text))
print("stripped raw:", repr(stripped_dummy_text))
print("length:", len(stripped_dummy_text))
print("first letter:", stripped_dummy_text[0])
print("last letter:", stripped_dummy_text[-1])
print("first 5 letters:", stripped_dummy_text[:5])
print("replace:", stripped_dummy_text.replace("world", "Leo"))

example = "banana"
print(example.upper())
print("count a:", example.count("a"))
print("index of first 'a':", example.find("a"))

name = "Joshua"
age = 23
# the '_' here is just a syntax sugar
pi = 3.141_592_653_5
print(name, age, pi)
print(f"{name} is {age} years old.")
print(f"pi in 2 decimals: {pi:.3f}")
print(f"name={name:<10} | age={age:>5}")
print(f"name={"bob":<10} | age={101:>5}")

a = 10
b = 3
print("a+b=", a+b)
print("a-b=", a-b)
print("a*b=", a*b)
print("a/b=", a/b)
print("a//b=", a//b)
print("a%b=", a%b)
print("a**b=", a**b)

# 10 / 3 = 3.33333333
# 3 * 3 = 9
# 10 - 9 = 1

# 10 / 2 = 5
# 2 * 5 = 10
# 10 - 10 = 0












