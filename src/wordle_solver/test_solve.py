"""Tests for main.py."""

# System Imports
import logging

# Relative Imports
import pytest
from solver import reduce_from_answer, solve


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


@pytest.mark.parametrize(
    "word_list,top_result",
    [
        (
            ["vouch", "couch", "pouch", "cough", "could", "dough", "bough", "would"],
            "couch",
        ),
    ],
)
def test_solve(caplog, word_list, top_result):
    """Test solve function works as expected."""

    # Set the logger capture level for debugging.
    caplog.set_level(logging.DEBUG)

    # Given - Parameterised Inputs

    # When
    _result = solve(word_list)

    # Then
    assert list(_result.keys())[0] == top_result
