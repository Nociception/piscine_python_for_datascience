# Subject
"""
Exercice 03: NULL not found
Turn-in directory : ex03/
Files to turn in : NULL_not_found.py
Allowed functions : None

Write a function that prints the object type of all types of "Null".
Return 0 if it goes well and 1 in case of error.
Your function needs to print all types of NULL.
Here's how it should be prototyped:
def NULL_not_found(object: any) -> int:

#your code here

Your tester.py:
from NULL_not_found import NULL_not_found
Nothing = None
Garlic = float("NaN")
Zero = 0
Empty = ''
Fake = False
NULL_not_found(Nothing)
NULL_not_found(Garlic)
NULL_not_found(Zero)
NULL_not_found(Empty)
NULL_not_found(Fake)
print(NULL_not_found("Brian"))

Expected output:
$>python tester.py | cat -e
Nothing: None <class 'NoneType'>$
Cheese: nan <class 'float'>$
Zero: 0 <class 'int'>$
Empty: <class 'str'>$
Fake: False <class 'bool'>$
Type not Found$
1$
$>
Running your function alone does nothing.
Expected output:
$>python NULL_not_found.py | cat -e
$>
"""


def NULL_not_found(object: any) -> int:
    """
    Receives an arg (object) of any type.
    If object is one of the following:
    None, nan(float), 0(int), ""(empty string), False
    Prints a specific text for each, and its type ;
    "Type not found" otherwise.
    Returns 0 if the type is found, 1 otherwise

    Usage:
    >>> NULL_not_found(0)
    Zero: 0 <class 'int'>
    0
    """

    DEBUG = 0
    if DEBUG:
        print("Debug part is commented, because of a forbidden import.\n"
              "Feel free to uncomment it.")
    #     import inspect
    #     print(f"function: {inspect.currentframe().f_code.co_name}"
    #           f" ; arg: {object} ; arg_type: {type(object)}")

    """
    A match case syntax does not fit here.
    case <python type such as str, float> leads to this error :
    SyntaxError: name capture 'str' makes remaining patterns unreachable
    """
    object_type = type(object)
    to_print = ""
    return_value = 0

    if object is None:
        to_print = f"Nothing: {object} {object_type}"
    elif object_type == float and object != object:
        to_print = f"Cheese: {object} {object_type}"
    elif object_type == int and object == 0:
        to_print = f"Zero: {object} {object_type}"
    elif object_type == str and object == "":
        to_print = f"Empty: {object_type}"
    elif object is False:
        to_print = f"Fake: {object} {object_type}"
    else:
        to_print = "Type not found"
        return_value = 1

    print(to_print)
    if DEBUG:
        print(f"return_value = {return_value}")
    return return_value
