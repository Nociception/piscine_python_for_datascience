import sys
from array2D import slice_me


def test_cases():
    """Return a list of test cases for slice_me."""

    asserror = "AssertionError: "
    error_not_list = asserror + "family is not a list."
    error_not_2d = asserror + "family list is not a 2D array."
    error_not_all_lists = asserror + "family must contain only lists."
    error_rows_length = asserror + "the rows are not the same length."
    error_invalid_types = asserror + "invalid type found among"\
        " item. Only the following types"\
        " are allowed: int, float, complex, bool"
    error_invalid_indexes = asserror + "Start or end"\
        " (or both) is not an integer."

    cases = [
        # Normal cases
        {
            "name": "Test 1: Subject case (standard slicing)",
            "function": slice_me,
            "args": ([[1.80, 78.4],
                      [2.15, 102.7],
                      [2.10, 98.5],
                      [1.88, 75.2]],
                     0,
                     2),
            "kwargs": {},
            "expected": [[1.8, 78.4], [2.15, 102.7]],
        },
        {
            "name": "Test 2: Subject case (negative slicing)",
            "function": slice_me,
            "args": ([[1.80, 78.4],
                      [2.15, 102.7],
                      [2.10, 98.5],
                      [1.88, 75.2]],
                     1,
                     -2),
            "kwargs": {},
            "expected": [[2.15, 102.7]],
        },
        {
            "name": "Test 3: Single row slicing",
            "function": slice_me,
            "args": ([[1.80, 78.4],
                      [2.15, 102.7],
                      [2.10, 98.5],
                      [1.88, 75.2]],
                     0,
                     1),
            "kwargs": {},
            "expected": [[1.8, 78.4]],
        },
        {
            "name": "Test 4: Empty slicing",
            "function": slice_me,
            "args": ([[1.80, 78.4],
                      [2.15, 102.7],
                      [2.10, 98.5],
                      [1.88, 75.2]],
                     1,
                     1),
            "kwargs": {},
            "expected": [],
        },
        {
            "name": "Test 5: Slicing beyond bounds",
            "function": slice_me,
            "args": ([[1.80, 78.4],
                      [2.15, 102.7],
                      [2.10, 98.5],
                      [1.88, 75.2]],
                     100,
                     200),
            "kwargs": {},
            "expected": [],
        },
        {
            "name": "Test 6: Full array slicing",
            "function": slice_me,
            "args": ([[1.80, 78.4],
                      [2.15, 102.7],
                      [2.10, 98.5],
                      [1.88, 75.2]],
                     0,
                     4),
            "kwargs": {},
            "expected": [[1.8, 78.4],
                         [2.15, 102.7],
                         [2.10, 98.5],
                         [1.88, 75.2]],
        },
        # Error cases
        {
            "name": "Test 7: Error - family is not a list",
            "function": slice_me,
            "args": ("not a list", 0, 2),
            "kwargs": {},
            "expected": error_not_list,
        },
        {
            "name": "Test 8: Error - family contains non-list elements",
            "function": slice_me,
            "args": ([[1.80, 78.4], (2.15, 102.7)], 0, 2),
            "kwargs": {},
            "expected": error_not_all_lists,
        },
        {
            "name": "Test 9: Error - rows have unequal lengths",
            "function": slice_me,
            "args": ([[1.80, 78.4], [2.15]], 0, 2),
            "kwargs": {},
            "expected": error_rows_length,
        },
        {
            "name": "Test 10: Error - invalid types in family elements",
            "function": slice_me,
            "args": ([[1.80, "not valid"], [2.15, 102.7]], 0, 2),
            "kwargs": {},
            "expected": error_invalid_types,
        },
        {
            "name": "Test 11: Error - start index is not an integer",
            "function": slice_me,
            "args": ([[1.80, 78.4], [2.15, 102.7]], "start", 2),
            "kwargs": {},
            "expected": error_invalid_indexes,
        },
        {
            "name": "Test 12: Error - end index is not an integer",
            "function": slice_me,
            "args": ([[1.80, 78.4], [2.15, 102.7]], 0, "end"),
            "kwargs": {},
            "expected": error_invalid_indexes,
        },
        # error_not_2d = asserror + "family must contain at least one row."
        {
            "name": "Test 13: Error - end index is not an integer",
            "function": slice_me,
            "args": ([[1.80, 78.4, 2.15, 102.7]], 0, 2),
            "kwargs": {},
            "expected": error_not_2d,
        }
    ]

    return cases


if __name__ == "__main__":
    sys.path.insert(0, "../../")
    from general_function_tester import general_function_tester

    debug = any(arg == "-debug" for arg in sys.argv)
    use_error_output = any(arg == "-use-error-output" for arg in sys.argv)

    if not debug:
        print("Use the -debug option for more details in the tests:\n"
              "python3 tester.py -debug\n")
        print("Use the -use-error-output option to"
              " validate errors with stderr:\n"
              "python3 tester.py -use-error-output\n")

    test_cases_list = test_cases()
    general_function_tester(test_cases_list, debug, use_error_output)
