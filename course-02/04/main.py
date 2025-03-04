import random

def print_matrix(matrix):
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            value = row[j]
            print(value, end=" ")
        print()

# Task 1
def create_matrix():
    m = [
        ['a', 'a', 'a', 'a'],
        ['a', 'a', 'a', 'a'],
        ['a', 'a', 'a', 'a'],
        ['a', 'a', 'a', 'a'],
    ]
    print(m)

# create_matrix()

def create_matrix2():
    m = []
    for i in range(4):
        temp = []
        for j in range(4):
            temp.append(random.randint(10, 21))
        m.append(temp)
    print_matrix(m)

#create_matrix2()

def generate_timetable():
    table = [["Biology","P.E","math","History","literature","physics","physics"],  # Monday
             ["math","History","grammar","English","literature","P.E","P.E"],  # Tuesday
             ["I.T","I.T","literature","grammar","math","chemistry"],  # Wednesday
             ["chemistry","I.T","","History","Biology","physics","English"],  # Thursday
             ["math","I.T","P.E","History","Biology"],]  # Friday

    time_table = []
    for _ in range(5):
        temp = []
        for _ in range(int(input("How much lesson will you have today? lesson = "))):
            lesson = input("Lesson: ")
            temp.append(lesson)
        time_table.append(temp)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    ind = 0
    for row in time_table:
        print(f"{days[ind]}: {row}")
        ind += 1
    print()
    print_matrix(time_table)
    print()
    print_matrix(table)

generate_timetable()
