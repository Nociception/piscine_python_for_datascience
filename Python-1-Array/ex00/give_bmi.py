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


def only_int_or_float_in_list(l: list) -> bool:
    """DOCSTRING"""

    return all(isinstance(x, (int, float)) for x in l)
    # (1) Further details about this check at the end of the file


def give_bmi(height: list[int | float],
             weight: list[int | float]) -> list[int | float]:
    """Receives two same-sized lists of numbers (int or float):
    height (no zero allowed) and weight.

    If:
    - both of the lists are not the same size
    - any element of any list is not int or float
    - there is one ore more zeros in height
    Raises an AssertionError

    Returns a list of bmi for each couple of value height[i], weight[i]"""

    DEBUG = 0

    def parsing(height: list[int | float],
                weight: list[int | float]) -> tuple[np.array, np.array]:
        """Receives and parses the two lists which give_bmi receives.
        Checks if :
        - They have the same size
        - They contains only int or float
        - There is no 0 in the height list (to prevent a ZeroDivisionError)
        
        Returns two numpy arrays generated from the two lists."""

        assert len(height) == len(weight), (
            "Error: Both of the list must be the same size."
        )
        assert only_int_or_float_in_list(height + weight), (
            "Error: Elements in both of the lists must be integers or floats."
        )
        assert all(height), ("Error: Numbers cannot be 0 in the height list.")

        return np.array(height), np.array(weight)

    try:
        height_arr, weight_arr = parsing(height, weight)
        if DEBUG:
            print(f"Function: give_bmi; height={height}; weight={weight}\n"
                  f"after parsing: height_arr={height_arr}; weight_arr={weight_arr}")
    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")

    bmi = weight_arr / (height_arr ** 2)
    return bmi.tolist()

def apply_limit(bmi: list[int | float], limit: int) -> list[bool]:
    """DOCSTRING"""

    def parsing(bmi: list[int | float], limit: int) -> np.ndarray:
        """DOCSTRING"""

        assert only_int_or_float_in_list(bmi), (
            "Error: Elements in both of the lists must be integers or floats."
        )
        assert isinstance(limit, int), ("Error: limit must be an integer.")

        return np.array(bmi)

    bmi_arr = parsing(bmi, limit)
    return (bmi_arr > limit).tolist()

"""
(1): Back to this check:
    assert all(isinstance(x, (int, float)) for x in height + weight), (
            "Elements in both of the lists must be integers or floats."
    )
    This check allows the lists to contain a mix of int and float.
    Because of numpy arrays can contain inly one type of data, if the list
    which is going to be turned into a numpy array contains a mix of
    int and float, int will be converted to float.
"""