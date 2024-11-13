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

    try:
        assert len(height) == len(weight), (
            "Both of the list must contain the same number of numbers."
        )
        assert all(isinstance(x, (int, float)) for x in height + weight), (
            "Elements in both of the lists must be integers or floats."
        )
        assert all(height), ("Numbers cannot be 0 in the height_list.")

        height_arr = np.array(height)
        weight_arr = np.array(weight)
        bmi = weight_arr / (height_arr ** 2)
        return bmi.tolist()

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")


def apply_limit(bmi: list[int | float], limit: int) -> list[bool]:
    """DOCSTRING"""

    bmi_arr = np.array(bmi)
    return (bmi_arr > limit).tolist()
