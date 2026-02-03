# Lists

l1 = [13, 22, 34, 6, 1, 12, 5]

for i in l1:
    print(f"item: {i}")

for i in l1:
    if i % 2 == 0:
        print(f"even: {i}")
    else:
        print(f"odd: {i}")

total = 0
for i in l1:
    total += i
print("total: ", total)

even_total = 0
odd_total = 0
for i in l1:
    if i % 2 == 0:
        even_total += i
    else:
        odd_total += i
print("even_total: ", even_total)
print("odd_total: ", odd_total)

text = ""
for i in range(1, 101):
    text += f"{i}, "
text = text[:-2]
print(text)

for i in range(1, 101, 2):
    print(i, end=", ")
print()

# Dictionaries

student = {
    "first_name": "Gary",
    "last_name": "D'Snake",
    "age": 20,
    "grade": "B"
}

print(student)
f_name = student["first_name"]
print(f_name)
l_name = student.get("last_name", "(no name)")
print(l_name)
m_name = student.get("middle_name", "(no name)")
print(f"{f_name} {m_name} {l_name}")

for k, v in student.items():
    print(f"{k}: {v}")

student["middle_name"] = "David"
print(student)

print(f"keys: {list(student.keys())}")

l2 = [4, 8, 15, 16, 17, 18]
l2[2:5] = [23, 42]
print(l2)

l3 = ["Malory", "Cheryl", "Ray", "Archer"]
print(l3[:2])
print(l3[:-2])