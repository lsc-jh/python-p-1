import math
import random
import matplotlib.pyplot as plt

print(math.pi)
print(math.e)
print(math.nan)
print(math.isnan(math.nan))
print(math.inf)

chances = 7
solution = random.randint(1, 101)
tip = 0

def check(num):
    if num > solution:
        return "Too big!"
    elif num < solution:
        return "Too small!"
    else:
        return "The game will end now..."

while tip != solution and chances > 0:
    tip = int(input("Enter your tip: "))
    check_result = check(tip)
    print(check_result)
    chances -= 1
if tip == solution:
    print("Congratulations! You have guessed the number!")
else:
    print("You have lost! The number was: ", solution)


def pie_chart(size, labels):
    plt.pie(size, labels=labels, autopct='%.2f%%')
    plt.show()
    plt.savefig("pie_chart.png")

n = int(input("How many games do you like? n = "))
games = []
likes = []
data = []
count = s = 0
for i in range(n):
    name = input("Game name: ")
    like = int(input("How much do you like it? (1-10 scale) "))
    games.append(name)
    likes.append(like)
    count += like

for i in range(n):
    s = likes[i] / count * 100
    s = round(s, 1)
    data.append(s)

pie_chart(data, games)
