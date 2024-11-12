# Subject
"""
Write a function that prints the object type of all types of "Null".
Return 0 if it goes well and 1 in case of error.
Your function needs to print all types of NULL
"""


def NULL_not_found(object: any) -> int:
    """DOCSTRING"""
    DEBUG = 0
    if DEBUG:
        import inspect
        print(f"function: {inspect.currentframe().f_code.co_name}"
              f" ; arg: {object} ; arg_type: {type(object)}")

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
