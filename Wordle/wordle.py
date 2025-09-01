import random
from words import words
import time
import keyboard

def color_letter(letter, color):
    colors = {
        "green": "\033[92m",   # bright green
        "yellow": "\033[93m",  # yellow
        "gray": "\033[90m",    # gray/dim
        "reset": "\033[0m"     # reset
    }
    return f"{colors[color]}{letter}{colors['reset']}"

def get_random_word(words):
    return random.choice(words).upper()

def startgame():
    correct_word = get_random_word(words)
    attempts = 6

    for attempt in range(1, attempts + 1):
        while True:
            guess = input(f"Attempt {attempt}/{attempts}: ").strip().upper()
            if len(guess) != 5 or not guess.isalpha():
                print("Please enter a valid 5-letter word.")
            else:
                break
        if guess == correct_word:
            print(color_letter(guess, 'green'))
            print(f"Congratulations! You've guessed the word '{correct_word}' correctly!")

            break
        else:
            feedback = [""] * 5
            word_chars = list(correct_word)  # mutable list to track consumed letters
            
            # First pass: greens
            for i in range(5):
                if guess[i] == correct_word[i]:
                    feedback[i] = color_letter(guess[i], "green")
                    word_chars[i] = None  # consume this letter

            # Second pass: yellows and grays
            for i in range(5):
                if feedback[i] == "":
                    if guess[i] in word_chars:
                        feedback[i] = color_letter(guess[i], "yellow")
                        word_chars[word_chars.index(guess[i])] = None  # consume one occurrence
                    else:
                        feedback[i] = color_letter(guess[i], "gray")

            print("".join(feedback))

        if attempt == attempts:
            print(f"Sorry, you've used all attempts. The correct word was '{correct_word}'.")

print("Welcome to Wordle!")
time.sleep(2)
print("You have 6 attempts to guess the 5-letter word.")
time.sleep(3)
print()
print("After each guess, letters will be colored as follows:")
print()
print(color_letter('G', 'green') + ": Correct letter in the correct position")
print(color_letter('Y', 'yellow') + ": Correct letter in the wrong position")
print(color_letter('X', 'gray') + ": Incorrect letter")
print()
time.sleep(5)
print("Press Enter to play!")
input()

while True:
    startgame()
    print("Press F to play again or any other key to exit!")

    event = keyboard.read_event(suppress=True)

    if event.event_type == "down" and event.name.lower() == "f":
        continue
    else:
        print("Thanks for playing!")
        break

        


