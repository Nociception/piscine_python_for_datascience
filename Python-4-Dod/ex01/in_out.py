# Subject
"""
Exercice 01: Outer_inner
Turn-in directory : ex01/
Files to turn in : in_out.py
Allowed functions : None

Write a function that returns the square of argument,
a function that returns the Exponentiation of argument
by himself and a function that takes as argument a number
and a function, it returns an object that when
called returns the result of the arguments calculation.

The prototype of functions is:
def square(x: int | float) -> int | float:
#your code here
def pow(x: int | float) -> int | float:
#your code here
def outer(x: int | float, function) -> object:
count = 0
def inner() -> float:
#your code here
"""


def square(x: int | float) -> int | float:
    """Returns x squared."""

    return x ** 2


def pow(x: int | float) -> int | float:
    """Returns x to the power of x."""

    return x ** x


def outer(x: int | float, function) -> object:
    """
    Returns an inner function.
    Then, my_counter = outer(3, square) makes this possible :
    my_counter()
    The variable became a callable object.
    Each call calls the inner function.
    """

    count = 0
    last_res = x

    def inner() -> float:
        """
        nonlocal is something similar compared to static in C language.
        As long as the object exists, the values stored in these variables
        are kept, and possibly reused.
        """

        nonlocal count
        nonlocal last_res
        res = function(last_res)
        last_res = res
        count += 1
        return res

    return inner
