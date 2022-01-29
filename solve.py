"""Solver."""

# System Imports
import logging
import os

# Relative Imports
from sandbox import solve, reduce

# Setup Logger
LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":

    if not os.path.exists('five_letter_words.txt'):
        raise Exception("Didn't find file called 'five_letter_words.txt'.")

    with open('five_letter_words.txt', 'r') as f:
        words = f.read().splitlines()

    # Solve
    while True:

        # Await guess.
        user_guess = input('Guess: ')
        feedback = input('Feedback: ')

        # Compute reduction.
        words = reduce(user_guess, feedback.upper(), words)

        if len(words) == 1:
            break

        # Print values.
        for guess, value in solve(words).items():
            print(f"{guess}: {value}")

