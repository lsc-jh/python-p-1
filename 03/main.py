text = input("Write something: ")
print(text)

len_of_var = len(text)

if len_of_var == 0:
    print("Nanana, you have to enter at least 1 character!!")
    exit(1)

if len_of_var >= 50:
    print("Oh, man, I didn't ask for an essay!!!!!")
    print("Next time, pls write shorter!")

print("Thx for the text!")

if "the" in text:
    print("Hahaha, please don't use the 'the' word!")

last_char = text[-1]

#if last_char != ".":
#   print("Oh oh, you left out the punctuation!!")

PUNCTUATION = [".", "!", "?"]

if last_char not in PUNCTUATION:
    print("Oh oh, you left out the punctuation!!")

#################
#               #
# Loops         #
#               #
#################

print("Numbers to 10:")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

for i in numbers:
    print(i)

for i in range(1, 51):
    print(i, end=", ")
print()

for c in text:
    print(c, end="")

print("\n")

i = 0
while i < 10:
    print(i, end=", ")
    i+=1
print()

while text:
    print(text)
    text = text[:-1]

#           1    2      3     4
list_1 = ["as", "sd", "s2", "asd"]

print(list_1[:])
print(list_1[2:])
print(list_1[:2])
print(list_1[:-1])
print()
print(list_1[:1])
print(list_1[:4])
print(list_1[1:])
print()
print(list_1[:-1])
print(list_1[-1:])



