"""Main."""

# System Imports
import os

# Relative Imports
from src.wordle_solver.solver import reduce_from_feedback, solve


if __name__ == "__main__":

    if not os.path.exists("five_letter_words.txt"):
        raise Exception("Didn't find file called 'five_letter_words.txt'.")

    with open("five_letter_words.txt", "r") as f:
        words = f.read().splitlines()

    # Solve
    while True:

        print("\n\nNew Round\n*********")

        # Await guess.
        user_guess = input("Guess: ")
        feedback = input("Feedback: ")

        # Compute reduction.
        words = reduce_from_feedback(user_guess, feedback.upper(), words)

        # Solve.
        print("\nSolving...")
        top_guesses = solve(words, 5).items()

        print("\n\nTop Guesses:")
        for guess, value in top_guesses:
            print(f"{guess}: {value}")

        if len(words) == 1:
            print("\nDone.")
            break