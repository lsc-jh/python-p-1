# Task 1 - Writing to a file

with open("hello.txt", "w") as f:
    f.write("Hello World\n")

# Task 1.1 Writing to a file
f = open("hello.txt", "a")
f.write("Hello World2\n")
f.close()

# Task 2 - Write and read
with open("hello2.txt", "w+") as f:
    f.write("How are you this fine evening?")
    f.seek(0)
    contents = f.read()
    print(contents)

with
