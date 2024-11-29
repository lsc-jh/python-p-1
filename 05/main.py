# Task 1

car_brands = [
    "BMW",
    "Honda",
    "Toyota",
    "Mercedes",
    "Subaru",
    "Koenigsegg",
    "Lamborghini"
]

VOWELS = ["a", "e", "i", "o", "u"]

for car_brand in car_brands:
    vowels = 0
    consonants = 0
    for letter in car_brand:
        if letter in VOWELS:
            vowels += 1
        else:
            consonants += 1

    properties = [
        f"Car Brand:\t | {car_brand}",
        f"Vowels:\t\t | {vowels}",
        f"Consonants:\t | {consonants}",
    ]

    dash_count = max([len(prop) for prop in properties]) + 1
    # TODO: Clean this up next class!!!!
    print()
    print(dash_count*"-")
    print("Name\t\t | Value")
    for prop in properties:
        print(prop)
    print(dash_count*"-")

