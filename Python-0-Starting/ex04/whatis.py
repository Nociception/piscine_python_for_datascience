#!/usr/bin/env python3

# Subject
"""
Exercice 04: The Even and the Odd
Turn-in directory : ex04/
Files to turn in : whatis.py
Allowed functions : sys or any other library that allows to receive the args

Create a script that takes a number as argument,
checks whether it is odd or even,
and prints the result.
If more than one argument is provided
or if the argument is not an integer, print am AssertionError.

Expected output:
$> python whatis.py 14
I'm Even.
$>
$> python whatis.py -5
I'm Odd.
$>
$> python whatis.py
$>
$> python whatis.py 0
I'm Even.
$>
$> python whatis.py Hi!
AssertionError: argument is not an integer
$>
$> python whatis.py 13 5
AssertionError: more than one argument is provided
$>
"""

import sys


def whatis() -> None:
    """Receives args from the CLI : python3 whatis.py arg1 arg2 arg...
    No arg does nothing, and gives back the prompt.
    More than one arg raises an AssertionError.
    Exactly one arg :
    it has to be intable (raises an AssertionError otherwise)
    Prints its parity :
    Returns nothing.

    Usage:
    $> python whatis.py 14
    I'm Even."""

    def parsing(argv: list) -> int:
        """Checks if exactly one argument is received,
        and if it is an integer.
        """

        nb_args = len(sys.argv) - 1
        if nb_args == 0:
            exit()
        assert nb_args == 1, ("more than one argument is provided")

        try:
            arg = int(sys.argv[1])
        except ValueError:
            raise AssertionError("argument must be an integer")

        return arg

    try:
        arg = parsing(sys.argv)
    except AssertionError as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        exit(1)

    parity = "Odd" if arg % 2 else "Even"
    print(f"I'm {parity}.")


if __name__ == "__main__":
    whatis()
