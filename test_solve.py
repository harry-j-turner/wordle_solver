"""Tests for solve.py."""

# System Imports
import logging
import os
import pytest

# Relative Imports
from solve import reduce, reduce_green, reduce_yellow


def _test_reduce_green(caplog):
    """Test green rules work as expected."""

    # Set the logger capture level for debugging.
    caplog.set_level(logging.INFO)

    # Given
    candidate = 'sheep'
    answer = 'spoon'
    word_list = ['spoon', 'plant', 'spade']

    # When
    reduced_word_list, _ = reduce_green(candidate, answer, word_list)

    # Then
    assert reduced_word_list == ['spoon', 'spade']


@pytest.mark.parametrize(
    "candidate, answer, word_list, reduced_list",
    [
        ('drink', 'spoon', ['blink', 'snoop', 'raven'], ['sNoop']),  # Rule 2.
        ('drink', 'spoon', ['snoop', 'spool'], ['sNoop']),  # Rule 3.
        ('coded', 'spoon', ['snoop', 'speak'], ['snOop']),  # Rule 3.
        ('spoon', 'chore', ['clock', 'crook', 'prawn'], ['clOck']),  # Rule 3. Multiple letters.
    ]
)
def test_reduce_yellow(caplog, candidate, answer, word_list, reduced_list):
    """Test yellow rules work as expected."""

    # Set the logger capture level for debugging.
    caplog.set_level(logging.INFO)

    # Given - Parameterised Inputs

    # When
    _reduced_list, _ = reduce_yellow(candidate, answer, word_list)

    # Then
    assert _reduced_list == reduced_list


@pytest.mark.parametrize(
    "candidate, answer, word_list, reduced_list",
    [
        ('abfgc', 'abcde', ['cdabc', 'abfgh', 'abcdg', 'abjck'], ['abjck']),  # Match first two, wrong position on last.
    ]
)
def test_reduce(caplog, candidate, answer, word_list, reduced_list):
    """Test overall reduce function works as expected."""

    # Set the logger capture level for debugging.
    caplog.set_level(logging.INFO)

    # Given - Parameterised Inputs

    # When
    _reduced_list = reduce(candidate, answer, word_list)

    # Then
    assert _reduced_list == reduced_list

