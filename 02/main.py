poem = input("Give me a poem:\n")
print(poem)

# Task 1 - Length of text
print(len(poem))
print(poem.__len__())

# Task 2 - Split the text
print(poem.split(' '))
print(poem.split('a'))

# Task 3 - Count a character
print(poem.count('a'))
print(poem.count('the'))

# Task 4 - Number checks
print("Number checks")
print(poem.isnumeric())
print(poem.isalpha())
print(poem.isalnum())
print(poem.isdigit())
print(poem.isdecimal())

# Task 5 - Case checks
print("Case checks")
print(poem.islower())
print(poem.isupper())
print(poem.istitle())
print(poem.isprintable())

# Task 6 - Start and end checks
print("Start and end checks")
print(poem.startswith('M'))
print(poem.endswith('w'))

# Case insensitive check
print(poem
      .lower()
      .upper()
      .lower()
      .startswith('m'))
