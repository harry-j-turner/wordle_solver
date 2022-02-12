"""Tests for main.py."""

# System Imports
import logging

# Relative Imports
import pytest
from solver import reduce_from_answer, reduce_from_feedback, solve


@pytest.mark.parametrize(
    "candidate, answer, word_list, reduced_list",
    [
        ("drink", "spoon", ["blink", "snoop", "raven"], ["snoop"]),
        ("drink", "spoon", ["snoop", "spool"], ["snoop"]),
        ("coded", "spoon", ["snoop", "speak"], ["snoop"]),
        ("spoon", "chore", ["clock", "crook", "prawn"], ["clock"]),
        ("abfgc", "abcde", ["cdabc", "abfgh", "abjck"], ["abjck"]),
    ],
)
def test_reduce_from_answer(caplog, candidate, answer, word_list, reduced_list):
    """Test reduce_from_answer works as expected."""

    # Set the logger capture level for debugging.
    caplog.set_level(logging.DEBUG)

    # Given - Parameterised Inputs

    # When
    _reduced_list = reduce_from_answer(candidate, answer, word_list)

    # Then
    assert _reduced_list == reduced_list


def test_reduce_from_feedback():
    """Test reduce_from_feedback function works as expected."""

    # Given
    words = ["could", "moult", "would", "wound", "young", "youth"]

    # When
    reduced_words = reduce_from_feedback("nobly", "_G_G_", words)

    # Then
    assert reduced_words == ["could", "moult", "would"]


@pytest.mark.parametrize(
    "guesses,feedback",
    [
        (["raise", "nobly", "could"], ["_____", "_G_G_", "GGGGG"]),
        (
            ["raise", "deter", "lower", "bluer", "ulcer"],
            ["y___y", "___GG", "Y__GG", "_GYGG", "GGGGG"],
        ),
    ],
)
def test_solve(caplog, guesses, feedback):
    """Test solve function works as expected."""

    # Set the logger capture level for debugging.
    caplog.set_level(logging.DEBUG)

    # Setup
    with open("../../five_letter_words.txt", "r") as f:
        words = f.read().splitlines()

    for i, (guess, feedback) in enumerate(zip(guesses, feedback)):

        words = reduce_from_feedback(guess, feedback.upper(), words)
        top_guess = list(solve(words, 1).keys())[0]

        try:
            assert guesses[i + 1] == top_guess
        except IndexError:
            pass

    assert len(words) == 1
