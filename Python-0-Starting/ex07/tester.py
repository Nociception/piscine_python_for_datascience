import sys
import os


def tests_dict() -> dict:
    """Return only the tests_dict
    First element of each list is the expected result"""
    tests = {
        "simple_word": ["... --- ...", "sos"],
        "phrase_with_spaces": [".- / -... --- -.-", '"a bok"'],
        "numbers": ["...-- ----. ..--- / ----. -----", '"392 90"'],
        "mixed_case": [".... . .-.. .-.. --- / .-- --- .-. .-.. -..",
                       '"Hello World"'],
        "invalid_characters": ["AssertionError: the arguments are bad",
                               "h$llo", "he##o"],
        "too_many_arguments": ["AssertionError: the arguments are bad",
                               "sos another_arg"]
    }
    return tests


if __name__ == "__main__":
    sys.path.insert(0, "../../")
    from general_tester import general_tester

    # Type here the file (with its extension) to test
    script_name = "sos.py"

    script_path = f"{os.getcwd()}/{script_name}"
    debug = any(arg == "-debug" for arg in sys.argv)
    if not debug:
        print("Use the -debug option for more details in the tests:\n"
              "python3 tester_sos.py -debug\n")
    general_tester(script_path, tests_dict(), debug)
