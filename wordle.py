# word_list_file = 'words_5.txt'
# word_list_file = "words_5_long.txt"
word_list_file = "nytimes_list.txt"
wordle_length = 5


def get_word_data() -> list[str]:
    with open(word_list_file) as possible_words:
        return [line.strip() for line in possible_words]


def constrain(
    all_possible_words: list[str],
    letters_to_remove: str,
    unpins: list[tuple[int, str]],
    pins: list[tuple[int, str]],
) -> list[str]:
    """
    given a list of words returns a new list that satisfies the given
    constraints
    :param all_possible_words: the input list of words
    :param letters_to_remove:  the returned list of words do not contain these letters
    :param unpins: the returned list of words contain these characters but not at the
                   position specified.
    :param pins: the returned list of words contain letters pinned to these position.
                 This is a list of tuples of the format (index, character) specifying that
                 index position `index` is fixed with character `character`
                 The first index position is 1 for convenience purposes
    :return: the new list that satisfies the above constraints
    """
    letters_to_contain = set(t[1] for t in unpins)
    return [
        word
        for word in all_possible_words
        if (
            not any(c for c in letters_to_remove if c in word)
        )  # filter out words that should not have the letters
        and all(
            c in word for c in letters_to_contain
        )  # filter words that should have these letters
        and all(
            word[pin[0] - 1] == pin[1] for pin in pins
        )  # filter words having these pins
        and all(
            word[unpin[0] - 1] != unpin[1] for unpin in unpins
        )  # filter words having these unpins
    ]


def calculate_letter_frequency(words: list[str]) -> dict[str, float]:
    """
    Given a dictionary of words return the letter frequency
    It is assumed that the dictionary only contains five letter words
    """
    freq = {letter: 0.0 for letter in "abcdefghijklmnopqrstuvwxyz"}
    for word in words:
        for c in word:
            freq[c] += 1

    letter_count = len(words) * wordle_length
    return {key: freq[key] / letter_count for key in freq}


def entropy(letter_frequency: dict[str, float], given_word: str) -> float:
    """
    Entropy of a word = sum of distict letters + sum of probablity of each
                        of the letters of the word given the letter
                        frequency
    """
    letter_set = set(given_word)
    return sum(letter_frequency[c] for c in letter_set) + len(letter_set)


def sort_by_entropy(words: list[str]) -> list[str]:
    """
    given a list of words returns the list sorted by the word entropy
    """
    frequency = calculate_letter_frequency(words)
    words_with_entropy = [(word, entropy(frequency, word)) for word in words]
    words_with_entropy.sort(key=lambda t: t[1], reverse=True)
    return [t[0] for t in words_with_entropy]


def get_tuples(in_string: str) -> list[tuple[int, str]]:
    """
    Given a string splits it into a list of tuples taking alternating
    elements of the string
    """
    return [
        (int(first), second) for first, second in zip(in_string[0::2], in_string[1::2])
    ]


if __name__ == "__main__":
    all_words = get_word_data()
    print(
        sort_by_entropy(
            constrain(
                all_possible_words=all_words,
                letters_to_remove="raielt",
                unpins=get_tuples('4s'),
                pins=get_tuples('2o4u5s'),
            )
        )
    )

