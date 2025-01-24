import sys
import os


def tests_dict() -> dict:
    """
    Returns only the tests_dict
    First element of each list is the expected result.
    """

    tests = {
        "basic": ["['Hello', 'World']", '"Hello the World" 4'],
        "none_long_enough": ['[]', '"Hello the World" 99'],
        "invalid_length_type": [
            "AssertionError: the arguments are bad",
            "3 'Hello the World'",
            "'Hello World' 'four'"
        ],
        "no_arguments": ["AssertionError: the arguments are bad", ""],
        "too_many_arguments": [
            "AssertionError: the arguments are bad",
            "'Hello World' 4 extra_arg"
        ],
        "invalid_characters": [
            "AssertionError: the arguments are bad",
            "'Hello, world!' 4",
            "'Hello\\nworld' 4"
        ],
    }
    return tests


if __name__ == "__main__":
    sys.path.insert(0, "../../")
    from general_tester import general_tester

    # Type here the file (with its extension) to test
    script_name = "filterstring.py"

    script_path = f"{os.getcwd()}/{script_name}"
    debug = any(arg == "-debug" for arg in sys.argv)
    if not debug:
        print("Use the -debug option for detailed tests:\n"
              "python3 tester.py -debug\n")
    general_tester(script_path, tests_dict(), debug)
