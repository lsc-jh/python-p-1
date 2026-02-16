import random

nice_messages = [
    "You're warming up!",
    "Not quite, but you're getting there!",
    "Nice try! Keep going!",
    "Everyone makes mistakes!"
]

sarcastic_messages = [
    "Bold guess. Wrong, but bold.",
    "Are you using a random number generator too?",
    "Interesting choice... very interesting.",
    "Have you tried guessing the *right* number?"
]

mean_messages = [
    "At this point, the computer is winning easily.",
    "This is getting painful to watch...",
    "Do you want a hint or a miracle?",
]

too_low_messages = [
    "Too low!",
    "Nope, lower!"
]

too_high_messages = [
    "Too high!",
    "Nope, higher!"
]


def main():
    best_score = None

    print("Welcome to the Number Guessing Game Deluxe!")
    while True:
        print("\nChoose difficulty:")
        print("1 - Easy (1-100")
        print("2 - Medium (1-500)")
        print("3 - Hard (1-1000)")

        while True:
            choice = input("Choose difficulty (1/2/3): ")
            try:
                difficulty = int(choice)
                if difficulty in (1, 2, 3):
                    break
                else:
                    print("Please choose 1, 2, or 3.")
            except ValueError:
                print("That's not a number! Please choose 1, 2, or 3.")

        max_number = 100
        if difficulty == 2:
            max_number = 500
        elif difficulty == 3:
            max_number = 1000

        secret = random.randint(1, max_number)
        attempts = 0

        print(f"I picked a number between 1 and {max_number}!")

        while True:
            while True:
                guess = input("Guess a number: ")
                try:
                    guess = int(guess)
                    if 1 <= guess <= max_number:
                        break
                    else:
                        print(f"Please guess a number between 1 and {max_number}.")
                except ValueError:
                    print("That's not a number! Please try again.")

            attempts += 1

            if attempts <= 3:
                mood_messages = nice_messages
            elif attempts <= 7:
                mood_messages = sarcastic_messages
            else:
                mood_messages = mean_messages

            if guess < secret:
                print(random.choice(too_low_messages))
                print(random.choice(mood_messages))
            elif guess > secret:
                print(random.choice(too_high_messages))
                print(random.choice(mood_messages))
            else:
                print("Well done! You guessed the number!")

                if best_score is None or attempts < best_score:
                    best_score = attempts
                    print(f"Congrats! You got a new best score: {best_score}")
                else:
                    print(f"Your score: {attempts}. Best score: {best_score}")

                break

        play_again = input("\nDo you want to play again? (y/N)") or "n"
        if play_again.lower() != "y":
            print("Thank you for playing! The computer will miss bullying you!")
            break


if __name__ == "__main__":
    main()
