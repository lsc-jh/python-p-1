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

# TODO: Refactor this into a constant
if last_char not in [".", "!", "?"]:
    print("Oh oh, you left out the punctuation!!")
