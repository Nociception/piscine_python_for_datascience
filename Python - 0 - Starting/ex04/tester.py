import sys
import os


def tests_dict() -> dict:
    """Return only the tests_dict
    First element of each list is the expected result"""
    tests = {
        "even": ["I'm Even.", "42", "0", "-0", "000000", "00000042",
                 "-0000042", "22", "1000002", "48", "50", "1004", "906"],
        "odd": ["I'm Odd.", "43", "-1", "1", "55", "333333333", "-9999",
                "005", "-55789", "-00057863"],
        "float_not_int": ["AssertionError: argument must be an integer",
                          "0.0", "4.2", "-2.4", "8898468.25522200"],
        "str_no_space": ["AssertionError: argument must be an integer",
                         "lol", "random_string"],
        "str_empty": ["", "", '', "    ", '     '],
        "str_with_spaces": [
            "AssertionError: more than one argument is provided",
            "random string", "   str    str        str  "]
    }
    return tests


if __name__ == "__main__":
    sys.path.insert(0, "../../")
    from general_tester import general_tester

    # Type here the file (with its extension) to test
    script_name = "whatis.py"

    script_path = f"{os.getcwd()}/{script_name}"
    debug = any(arg == "-debug" for arg in sys.argv)
    if not debug:
        print("Use the -debug option for more details in the tests:\n"
              "python3 tester.py -debug\n")
    general_tester(script_path, tests_dict(), debug)
