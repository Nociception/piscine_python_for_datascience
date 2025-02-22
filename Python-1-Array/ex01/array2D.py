# Subject
"""
Exercice 01: 2D array
Turn-in directory : ex01/
Files to turn in : array2D.py
Allowed functions : numpy or any lib of table manipulation

Write a function that takes as parameters a 2D array,
prints its shape, and returns a truncated version of the array
based on the provided start and end arguments.
You must use the slicing method.
You have to handle error cases if the lists are not the same size,
are not a list ...

The prototype of function is:
def slice_me(family: list, start: int, end: int) -> list:
#your code here

Your tester.py:
from array2D import slice_me
family = [[1.80, 78.4],
[2.15, 102.7],
[2.10, 98.5],
[1.88, 75.2]]
print(slice_me(family, 0, 2))
print(slice_me(family, 1, -2))

Expected output:
$> python test_array2D.py
My shape is : (4, 2)
My new shape is : (2, 2)
[[1.8, 78.4], [2.15, 102.7]]
My shape is : (4, 2)
My new shape is : (1, 2)
[[2.15, 102.7]]
$>
"""

import numpy as np


def slice_me(family: list, start: int, end: int) -> list:
    """
    Takes a 2D list and returns a sliced version
    of it based on the provided indices.

    The function validates the input `family` to ensure it is a 2D list where:
    - All rows are lists of equal length.
    - Elements in the 2D list are of specific
    valid types (int, float, complex, bool).
    - `start` and `end` are integers representing slicing indices.

    The function prints the shape of the original and the sliced 2D array.

    Args:
        family (list): A 2D list of numbers
        (int, float, complex, bool) where all rows are of equal length.
        start (int): The starting index for slicing.
        end (int): The ending index for slicing.

    Returns:
        list: A truncated 2D list based on the slicing indices.

    Raises:
        AssertionError: If `family` is not a 2D list,
        the rows have unequal lengths, invalid types are present,
        or `start` and `end` are not integers.

    Examples:
        >>> family = [[1.80, 78.4], [2.15, 102.7], [2.10, 98.5], [1.88, 75.2]]
        >>> slice_me(family, 0, 2)
        My shape is : (4, 2)
        My new shape is : (2, 2)
        [[1.8, 78.4], [2.15, 102.7]]

        >>> slice_me(family, 1, -2)
        My shape is : (4, 2)
        My new shape is : (1, 2)
        [[2.15, 102.7]]
    """

    def parsing(family: list, start: int, end: int) -> np.ndarray:
        """
        Validates the input parameters
        and converts `family` to a 2D numpy array.

        Args:
            family (list): A 2D list of numbers (int, float, complex, or bool).
            start (int): The starting index for slicing.
            end (int): The ending index for slicing.

        Returns:
            np.ndarray: A 2D numpy array representation of `family`.

        Raises:
            AssertionError: If any of the validation checks fail.
        """

        assert isinstance(family, list), ("family is not a list.")
        assert len(family) >= 2, ("family list is not a 2D array.")
        assert all(isinstance(row, list) for row in family), (
                "family must contain only lists."
            )
        assert all(len(family[0]) == len(row) for row in family), (
            "the rows are not the same length."
        )

        VALID_TYPES = (int, float, complex, bool)
        assert all(
            all(isinstance(elt, VALID_TYPES) for elt in row) for row in family
        ), (
            "invalid type found among item. Only the following types"
            " are allowed: int, float, complex, bool"
        )

        assert isinstance(start, int) and isinstance(end, int), (
            "Start or end (or both) is not an integer."
        )

        return np.array(family)

    try:
        family_array = parsing(family, start, end)
        print(f"My shape is : {family_array.shape}")

        sliced_family = family_array[start:end]
        print(f"My new shape is : {sliced_family.shape}")

        return sliced_family.tolist()

    except AssertionError as e:
        print(f"{type(e).__name__}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
