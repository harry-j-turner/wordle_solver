"""Main."""

# System Imports
import os

# Relative Imports
from src.wordle_solver.solver import value


if __name__ == "__main__":

    if not os.path.exists("five_letter_words.txt"):
        raise Exception("Didn't find file called 'five_letter_words.txt'.")

    with open("five_letter_words.txt", "r") as f:
        words = f.read().splitlines()

    print(value('raise', words))
    print(value('soare', words))