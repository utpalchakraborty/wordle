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


if __name__ == "__main__":
    all_words = get_word_data()

    print(
        constrain(
            all_possible_words=all_words,
            letters_to_remove="f",
            letters_to_contain="otn",
            pins=[(2, "u")],
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

