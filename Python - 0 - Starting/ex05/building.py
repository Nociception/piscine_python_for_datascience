#!/usr/bin/env python3

import sys


def main() -> None:
    """
    Counts different sort of character (upper-case characters,
    lower-case characters, punctuation characters,
    digits and spaces)in the text argument received from the shell,
    and prints the result.

    If no argument is received from the shell, it is possible to
    type it on several lines.
    Each \\n typed through the Entry key is turned into a space.
    Send an EOF signal (through Ctrl+D) to end your text.
    """

    DEBUG = 0

    def get_input() -> str:
        """Gets the input in case of no argument is provided in the CLI.
        Each carriage return is turned into a space.
        End of capture occurs with an EOF signal (lauched with Ctrl+D).
        Returns a string which contains each line, space (not \\n) separated.
        """
        print("What is the text to count?")
        text = list()
        while True:
            try:
                s = input()
                text.append(s) if s else text.append(' ')
            except EOFError:
                break
        text = ''.join(text)
        if len(text) == 0:
            print("No input provided.")
            exit(1)
        return text

    def building_count_function(text: str) -> None:
        """
        Displays several numbers, according to the text(a string)
        argument received ; number of :
        - upper letter(s)
        - lower letter(s)
        - punctuation mark(s)
        - space(s)
        - digit(s)
        """
        punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        criteria = {"upper letters": lambda c: c.isupper(),
                    "lower letters": lambda c: c.islower(),
                    "punctuation marks": lambda c: c in punctuation,
                    "spaces": lambda c: c.isspace(),
                    "digits": lambda c: c.isdigit()}

        counts = {
            name: sum(1 for c in text if check(c))
            for name, check in criteria.items()}

        print(f"The text contains {len(text)} characters:")
        for name, count in counts.items():
            print(f"{count} {name}")

    nb_args = len(sys.argv) - 1
    try:
        assert nb_args < 2, ("more than one argument is provided")
    except AssertionError as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        exit(1)

    text = ""
    if nb_args == 0:
        text = get_input()
    elif nb_args == 1:
        text = sys.argv[1]
    if DEBUG:
        print(f"text = {text}")

    building_count_function(text)


if __name__ == "__main__":
    main()
