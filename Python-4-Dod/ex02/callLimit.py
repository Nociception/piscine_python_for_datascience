# Subject
"""
Exercice 02: my first decorating
Turn-in directory : ex02/
Files to turn in : callLimit.py
Allowed functions : None
Write a function that takes as argument
a call limit of another function and blocks
its execution above a limit.
The prototype of functions is:
def callLimit(limit: int):
count = 0
def callLimiter(function):
def limit_function(*args: Any, **kwds: Any):
#your code here

Wrappers
"""

from typing import Any


def callLimit(limit: int):
    """
    Used such as:
    @callLimit(3)
    def f():
        print ("f()")

    callLimit receives f as a parameter, and passes it to call_limiter.

    It is like this was called : callLimit(3)(f)
    which is equivalent to call callLimiter with the decorated function
    as a parameters.
    """

    count = 0

    def callLimiter(function):
        """
        The actual decorator that wraps the given function.
        It receives the function to be decorated.

        Returns a wrapper.
        """

        def limit_function(*args, **kwds: Any):
            """
            Wrapper function that tracks the call count, and
            allows or not the function running.
            """

            nonlocal count

            if count >= limit:
                print(f"Error: {function} called too many times.")
            else:
                count += 1
                return function(*args, **kwds)

        return limit_function

    return callLimiter
