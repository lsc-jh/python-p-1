# Task: List creation

list1 = list()
print(list1)

list11 = []
print(list11)

# Task 1.1 List creation with values

list2 = [1,2,3,4,5]
print(list2)

list3 = list2[:]
print(list3)

# Task 2 

sentence = []  # type: list[str]

#for i in range(0, 10):
    #sentence.append(input("Enter a word: "))

print(" ".join(sentence))

# Task 3

sentence = []
word_count = 0
SPACE = " "
while word_count < 10:
    word = input(f"Enter {word_count + 1}. word: ")
    if SPACE in word:
        choice = input("I found a whitespace in your word, do you want me to trunkate them or you'll write a new word? (T/n)\nChoice: ")
        if "n" == choice or "N" == choice:
            continue
        else:
            word = word.replace(" ", "")
    sentence.append(word)
    word_count+=1


print(" ".join(sentence))
