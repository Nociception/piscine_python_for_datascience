# Subject
"""
Exercice 00: Give my BMI
Turn-in directory : ex00/
Files to turn in : give_bmi.py
Allowed functions : numpy or any lib of table manipulation

Your function, give_bmi, take 2 lists of integers or floats in input
and returns a list of BMI values.
Your function, apply_limit, accepts a list of integers or floats
and an integer representing a limit as parameters.
It returns a list of booleans (True if above the limit).
You have to handle error cases if the lists are not the same size,
are not int or float...

The prototype of functions is:
def give_bmi(height: list[int | float], weight: list[int | float])
 -> list[int | float]:
#your code here
def apply_limit(bmi: list[int | float], limit: int) -> list[bool]:
#your code here

Your tester.py:
from give_bmi import give_bmi, apply_limit
height = [2.71, 1.15]
weight = [165.3, 38.4]
bmi = give_bmi(height, weight)
print(bmi, type(bmi))
print(apply_limit(bmi, 26))

Expected output:
$> python tester.py
[22.507863455018317, 29.0359168241966] <class 'list'>
[False, True]
$>
"""

import numpy as np


def only_int_or_float_in_list(li: list) -> bool:
    """Checks if all elements in the list are either integers or floats.

    Args:
        l (list): The list to check.

    Returns:
        bool: True if all elements are integers or floats, False otherwise.
    """

    return all(isinstance(x, (int, float)) for x in li)
    # (1) Further details about this check at the end of the file


def give_bmi(height: list[int | float],
             weight: list[int | float]) -> list[int | float]:
    """Calculates BMI values for corresponding heights and weights.

    Args:
        height (list[int | float]): A list of heights (in meters).
        weight (list[int | float]): A list of weights (in kilograms).

    Returns:
        list[int | float]: A list of BMI values or an empty list
        if an error occurs.
    """

    DEBUG = 0

    def parsing(height: list[int | float],
                weight: list[int | float]) -> tuple[np.array, np.array]:
        """Validates input data and converts it to numpy arrays.

        Args:
            height (list[int | float]): Heights.
            weight (list[int | float]): Weights.

        Returns:
            tuple[np.array, np.array]: Converted numpy arrays
            of heights and weights.
        """

        assert all(isinstance(x, list) for x in (height, weight)), (
            "Both of the arguments must be lists."
        )
        assert len(height) == len(weight), (
            "Both of the list must be the same size."
        )
        assert only_int_or_float_in_list(height + weight), (
            "Elements in both of the lists must be integers or floats."
        )
        assert all(height), ("Numbers cannot be 0 in the height list.")

        return np.array(height), np.array(weight)

    try:
        height_arr, weight_arr = parsing(height, weight)
        if DEBUG:
            print(f"Function: give_bmi; height={height}; weight={weight}\n"
                  f"after parsing: height_arr={height_arr};"
                  f" weight_arr={weight_arr}")
    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
        return []

    bmi = weight_arr / (height_arr ** 2)
    return bmi.tolist()


def apply_limit(bmi: list[int | float], limit: int) -> list[bool]:
    """Applies a limit to BMI values to determine if they exceed the limit.

    Args:
        bmi (list[int | float]): A list of BMI values.
        limit (int): The limit to compare against.

    Returns:
        list[bool]: A list of booleans indicating if
        each BMI exceeds the limit.
    """

    def parsing(bmi: list[int | float], limit: int) -> np.ndarray:
        """Validates input data and converts it to a numpy array.

        Args:
            bmi (list[int | float]): BMI values.
            limit (int): The limit to compare against.

        Returns:
            np.ndarray: Converted numpy array of BMI values.
        """

        assert isinstance(bmi, list), ("bmi arg must be a list.")
        assert only_int_or_float_in_list(bmi), (
            "Elements in both of the lists must be integers or floats."
        )
        assert isinstance(limit, int), ("limit must be an integer.")

        return np.array(bmi)

    try:
        bmi_arr = parsing(bmi, limit)
        return (bmi_arr > limit).tolist()

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
        return []


"""
(1): Back to this check:
    assert all(isinstance(x, (int, float)) for x in height + weight), (
            "Elements in both of the lists must be integers or floats."
    )
    This check allows the lists to contain a mix of int and float.
    Because of numpy arrays can contain only one type of data, if the list
    which is going to be turned into a numpy array contains a mix of
    int and float, int will be converted to float.
"""
