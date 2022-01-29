"""Solver."""

# System Imports
import logging
import re
import os
import tqdm

# Setup Logger
logging.basicConfig(level=logging.WARNING)
LOGGER = logging.getLogger(__name__)


def capitalise(s, n):
    return ''.join([s[:n], s[n].upper(), s[n + 1:]])


def eliminate_green(guess: str, answer: str, word_list: list[str]) -> tuple[list[str],str]:
    """Reduce word list based on green matches.

    Rule: 1
    If letter x matches at position i, then remove from word_list all that don't
    contain letter x at position i.

    Args:
        :param guess: The guess word.
        :param answer: The answer word.
        :param word_list: A list of words containing the answer and guess.

    Returns:
        :return: A eliminated list of words that are not compatible with the guess/answer.
    """
    # Create a copy of the wordlist.
    _word_list = list(word_list)

    for i in range(5):

        # Rule 1 - If letter matches at position, remove all that don't match.
        if (x := guess[i]) == answer[i]:
            _word_list = [capitalise(w, w.index(x)) for w in _word_list if w[i] == x]
            answer = capitalise(answer, answer.index(x))
            LOGGER.info(f"[{answer}] Rule 1: Letter {x} matched at position {i}. [{answer}]{_word_list}")

    return _word_list, answer


def eliminate_yellow(guess: str, answer: str, word_list: list[str]) -> tuple[list[str], str]:
    """Reduce word list based on yellow matches.

    Rule 2:
    If letter x is not in the answer at all, then remove from the word_list all
    words that contain that letter.

    Rule 3:
    If the letter x is in the answer and not yet accounted for, then remove from the
    word_list all words that do not contain that letter.

    Handling Multiple Letters:
    Once matched, capitalise them so that they aren't matched again.

    Args:
        :param guess: The guess word.
        :param answer: The answer word.
        :param word_list: A list of words containing the answer and guess.

    Returns:
        :return: A eliminated list of words that are not compatible with the guess/answer.
    """
    # Create a copy of the wordlist.
    _word_list = list(word_list)

    for i in range(5):

        # Rule 2 - If not in answer, remove all that contain the letter.
        if (x := guess[i]) not in answer:
            _word_list = [w for w in _word_list if x not in w]
            LOGGER.info(f"[{answer}] Rule 2: Letter {x} is not in the answer. [{answer}]{_word_list}")

        # Rule 3 - If in answer remove all that don't contain the letter.
        else:
            _word_list = [capitalise(w, w.index(x)) for w in _word_list if x in w]
            answer = capitalise(answer, answer.index(x))
            LOGGER.info(f"[{answer}] Rule 3: Letter {x} in the wrong position. [{answer}]{_word_list}")

    return _word_list, answer


def eliminate(guess: str, answer: str, word_list: list[str]) -> list[str]:
    """

    Args:
        :param guess: The guess word.
        :param answer: The answer word.
        :param word_list: A list of words containing the answer and guess.

    Returns:
        :return: A eliminated list of words that are not compatible with the guess/answer.
    """

    # Create a copy of the wordlist.
    _word_list = list(word_list)
    LOGGER.info(f"[{answer}]{_word_list}")

    # First pass - eliminate greens.
    _word_list, _answer = eliminate_green(guess, answer, _word_list)

    # Second pass - eliminate yellows.
    _word_list, _answer = eliminate_yellow(guess, _answer, _word_list)

    # Convert to lower case.
    _word_list = [w.lower() for w in _word_list]

    return _word_list


def value(guess: str, word_list: list[str]) -> float:
    """Compute the value for a guess.

    For a given guess and word list, compute the expected size of the eliminated word list if you
    had made that guess. It assumes each word in the word list is the answer in turn and computes
    the eliminated word list size if that answer were correct. Given that the answer could be any of
    the words with equal probability, I take the average.

    :param guess: The word to compute the value for.
    :param word_list: The current valid word list.
    :return: The expected size of the word list should you make this guess.
    """

    eliminated_word_list_sum = 0

    # For each word in the word list, assume it's the answer and compute reduction.
    for answer in word_list:

        eliminated_word_list = eliminate(guess, answer, word_list)
        eliminated_word_list_sum += len(eliminated_word_list)

    return eliminated_word_list_sum / len(word_list)


def reduce(guess: str, feedback: str, word_list: list[str]) -> list[str]:
    """Reduce the size of the word list for a given guess and feedback.

    Assume the user has input a guess into Wordle and received feedback, this function
    filters the wordlist and returns the reduced set.

    Format:
    The feedback must be a string of five characters containing only _, G, Y.
    _: Black feedback from Wordle.
    G: Green feedback from Wordle.
    Y: Yellow feedback from Wordle.

    :param guess: The guess that was entered into Wordle.
    :param feedback: The feedback received from Wordle. See format above.
    :param word_list: The current word list containing valid candidate words.
    :return: A reduced word list with invalid words filtered out.
    """
    # Validate inputs.
    assert len(guess) == 5
    assert len(feedback) == 5
    assert set(feedback) <= {'_', 'G', 'Y'}

    # Create a copy of the wordlist.
    _word_list = list(word_list)

    # Filter word list for each letter.
    for i in range(5):

        # Rule 1 - If letter matches at position, remove all that don't match.
        if feedback[i] == 'G':
            _word_list = [capitalise(w, i) for w in _word_list if w[i] == guess[i]]

        # Rule 2 - If not in answer, remove all that contain the letter.
        elif feedback[i] == '_':
            _word_list = [w for w in _word_list if guess[i] not in w]
            LOGGER.info(f"Rule 2: {guess[i]} not in the answer.")

        # Rule 3 - If in answer remove all that don't contain the letter.
        else:
            _word_list = [capitalise(w, w.index(guess[i])) for w in _word_list if guess[i] in w]

    # Convert back to lower case.
    return [w.lower() for w in _word_list]


def solve(word_list: list[str], top_k: int = 10) -> dict[str, float]:
    """Solve for the most valuable words in the word_list.

    For every word in the word list, compute the value, which is the expected reduction in the size
    of the word list should you choose that word. Choose the top K and return the results. (In
    practice you'd simply pick the best, but show the top K just for fun).

    :param word_list: The current word list of valid candidates.
    :param top_k: The number of words/value pairs to return in the results.
    :return: Returns a dictionary mapping words to values.
    """

    # Keep track of the results.
    result_set = set()

    # For every word in the list, compute the value.
    LOGGER.info("Solving.")
    for guess in tqdm.tqdm(word_list):
        result_set.add((guess, value(guess, word_list)))

    # Convert the result set into a dictionary and return.
    sorted_result_set = sorted(result_set, key=lambda k: k[1])
    return {k: v for k, v in sorted_result_set[:top_k]}
