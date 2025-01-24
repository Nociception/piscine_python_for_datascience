# Subject

"""
Exercice 07: Dictionaries SoS
Turn-in directory : ex07/
Files to turn in : sos.py
Allowed functions : sys or any other library that allows to receive the args

Make a program that takes a string as an argument
and encodes it into Morse Code.
• The program supports space and alphanumeric characters
• An alphanumeric character is represented by dots . and dashes -
• Complete morse characters are separated by a single space
• A space character is represented by a slash /

You must use a dictionary to store your morse code.
NESTED_MORSE = { " ": "/ ",
"A": ".- ",
...

If the number of arguments is different from 1,
or if the type of any argument is wrong,
the program prints an AssertionError.

$> python sos.py "sos" | cat -e
... --- ...$
$> python sos.py 'h$llo'
AssertionError: the arguments are bad
$>
"""

import sys


def main() -> None:
    """
    Receives exactly one arg(text, a string) from the CLI.
    text string has to contains only alphanumeric characters and spaces.
    Prints the text encoded into Morse Code.

    If:
        the number of arguments is not one
        the text string contains wrong characters
    It leads to an AssertionError.

    Returns nothing.

    Usage:
    $> python sos.py "sos" | cat -e
    ... --- ...$
    """

    DEBUG = 0

    NESTED_MORSE = {" ": "/",
                    "A": ".-",
                    "B": "-...",
                    "C": "-.-.",
                    "D": "-..",
                    "E": ".",
                    "F": "..-.",
                    "G": "--.",
                    "H": "....",
                    "I": "..",
                    "J": ".---",
                    "K": "-.-",
                    "L": ".-..",
                    "M": "--",
                    "N": "-.",
                    "O": "---",
                    "P": ".--.",
                    "Q": "--.-",
                    "R": ".-.",
                    "S": "...",
                    "T": "-",
                    "U": "..-",
                    "V": "...-",
                    "W": ".--",
                    "X": "-..-",
                    "Y": "-.--",
                    "Z": "--..",
                    "0": "-----",
                    "1": ".----",
                    "2": "..---",
                    "3": "...--",
                    "4": "....-",
                    "5": ".....",
                    "6": "-....",
                    "7": "--...",
                    "8": "---..",
                    "9": "----.",
                    }

    text = ""
    try:
        only_error_text = "the arguments are bad"

        assert len(sys.argv) - 1 == 1, (only_error_text + f"{DEBUG*'(1)'}")

        text = sys.argv[1]
        assert all(c.isalnum() or c.isspace() for c in text), (
            only_error_text + f"{DEBUG*'(2)'}")
    except AssertionError as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        exit(1)

    text = text.upper()
    print(' '.join(NESTED_MORSE[c] for c in text))


if __name__ == "__main__":
    main()
