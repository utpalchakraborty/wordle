# word_list_file = 'words_5.txt'
# word_list_file = "words_5_long.txt"
word_list_file = "nytimes_list.txt"


def get_word_data() -> list[str]:
    with open(word_list_file) as possible_words:
        return [line.strip() for line in possible_words]


def constrain(
    all_possible_words: list[str],
    letters_to_remove: str,
    letters_to_contain: str,
    pins: list[tuple[int, str]],
) -> list[str]:
    """
    given a list of words returns a new list that satisfies the given
    constraints
    :param all_possible_words: the input list of words
    :param letters_to_remove:  the returned list of words do not contain these leters
    :param letters_to_contain: the returned list of words do contain these letters
    :param pins: the returned list of words contained letters pinned to these position.
                 This is a list of tuples of the format (index, character) specifying that
                 index position `index` is fixed with character `character`
                 The first index position is 1 for convenience purposes
    :return: the new list that satisfies the above constraints
    """
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

    letter_count = len(words) * 5
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


if __name__ == "__main__":
    all_words = get_word_data()
    print(sort_by_entropy(all_words))

    print(
        sort_by_entropy(
            constrain(
                all_possible_words=all_words,
                letters_to_remove="f",
                letters_to_contain="otn",
                pins=[(2, "u")],
            )
        )
    )

    print(
        constrain(
            all_possible_words=all_words,
            letters_to_remove="craneo",
            letters_to_contain="",
            pins=[(1, "s"), (2, "p"), (5, "l")],
        )
    )
