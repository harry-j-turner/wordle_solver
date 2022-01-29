"""Solver."""

# Third Party Imports
import tqdm


# Utility Functions
###################


def capitalise(string: str, n: int) -> str:
    """Capitalise the nth letter in the string.

    Args:
        string: The input string which will be altered.
        n: The index indicating which letter to capitalise.

    Returns:
        A new string with the nth letter capitalised.
    """
    return "".join([string[:n], string[n].upper(), string[n + 1 :]])


# Rules
#######


def green_filter(word_list: list[str], i: int, x: str) -> list[str]:
    """Keep words that contain letter x at position i."""
    return [capitalise(w, w.index(x)) for w in word_list if w[i] == x]


def black_filter(word_list: list[str], x: str) -> list[str]:
    """Keep words that don't contain letter x."""
    return [w for w in word_list if x not in w]


def yellow_filter(word_list: list[str], x: str) -> list[str]:
    """Keep words that contain letter x."""
    return [capitalise(w, w.index(x)) for w in word_list if x in w]


# Reducers
##########


def reduce_from_answer(guess: str, answer: str, word_list: list[str]) -> list[str]:
    """Reduce word list based on the combination of guess and answer.

    This reduce function takes a word list and returns a reduced word list by filtering.
    It does so by assuming that the answer is known, and computing the reduction in word
    list achieved by comparing the guess to the answer.

    Args:
        guess: The guess word.
        answer: The answer word.
        word_list: A list of words containing the answer and guess.

    Returns:
        A eliminated list of words that are not compatible with the guess/answer.
    """

    # Create a copy of the wordlist and answer.
    _word_list = list(word_list)

    # First pass - eliminate greens.
    for i in range(5):

        # Rule 1 - If letter matches at position, remove all that don't match.
        if (x := guess[i]) == answer[i]:
            _word_list = green_filter(_word_list, i, x)
            answer = capitalise(answer, answer.index(x))

    # Second pass - eliminate yellows.
    for i in range(5):

        # Rule 2 - If not in answer, remove all that contain the letter.
        if (x := guess[i]) not in answer:
            _word_list = black_filter(_word_list, x)

        # Rule 3 - If in answer remove all that don't contain the letter.
        else:
            _word_list = yellow_filter(_word_list, x)
            answer = capitalise(answer, answer.index(x))

    # Convert to lower case.
    _word_list = [w.lower() for w in _word_list]

    return _word_list


def reduce_from_feedback(guess: str, feedback: str, word_list: list[str]) -> list[str]:
    """Reduce the size of the word list for a given guess and feedback.

    Assume the user has input a guess into Wordle and received feedback, this function
    filters the wordlist and returns the reduced set.

    Format:
    The feedback must be a string of five characters containing only _, G, Y.
    _: Black feedback from Wordle.
    G: Green feedback from Wordle.
    Y: Yellow feedback from Wordle.

    Args:
        guess: The guess that was entered into Wordle.
        feedback: The feedback received from Wordle. See format above.
        word_list: The current word list containing valid candidate words.

    Returns:
        A reduced word list with invalid words filtered out.
    """
    # Validate inputs.
    assert len(guess) == 5
    assert len(feedback) == 5
    assert set(feedback) <= {"_", "G", "Y"}

    # Create a copy of the wordlist.
    _word_list = list(word_list)

    # Filter word list for each letter.
    for i in range(5):

        # Rule 1 - If letter matches at position, remove all that don't match.
        if feedback[i] == "G":
            _word_list = green_filter(_word_list, i, guess[i])

        # Rule 2 - If not in answer, keep words that don't contain the letter.
        elif feedback[i] == "_":
            _word_list = black_filter(_word_list, guess[i])

        # Rule 3 - If in answer remove all that don't contain the letter.
        else:
            _word_list = yellow_filter(_word_list, guess[i])

    # Convert back to lower case.
    return [w.lower() for w in _word_list]


def value(guess: str, word_list: list[str]) -> float:
    """Compute the value for a guess.

    For a given guess and word list, compute the expected size of the eliminated word list if you
    had made that guess. It assumes each word in the word list is the answer in turn and computes
    the eliminated word list size if that answer were correct. Given that the answer could be any of
    the words with equal probability, I take the average.

    Args:
        guess: The word to compute the value for.
        word_list: The current valid word list.

    Returns:
        The expected size of the word list should you make this guess.
    """

    eliminated_word_list_sum = 0

    # For each word in the word list, assume it's the answer and compute reduction.
    for answer in word_list:

        eliminated_word_list = reduce_from_answer(guess, answer, word_list)
        eliminated_word_list_sum += len(eliminated_word_list)

    return eliminated_word_list_sum / len(word_list)


def solve(word_list: list[str], top_k: int = 10) -> dict[str, float]:
    """Solve for the most valuable words in the word_list.

    For every word in the word list, compute the value, which is the expected reduction in the size
    of the word list should you choose that word. Choose the top K and return the results. (In
    practice you'd simply pick the best, but show the top K just for fun).

    Args:
        word_list: The current word list of valid candidates.
        top_k: The number of words/value pairs to return in the results.

    Returns:
        Returns a dictionary mapping words to values.
    """

    # Keep track of the results.
    result_set = set()

    # For every word in the list, compute the value.
    for guess in tqdm.tqdm(word_list):
        result_set.add((guess, value(guess, word_list)))

    # Convert the result set into a dictionary and return.
    sorted_result_set = sorted(result_set, key=lambda k: (k[1], k[0]))
    return {k: v for k, v in sorted_result_set[:top_k]}
