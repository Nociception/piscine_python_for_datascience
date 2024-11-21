import sys
from give_bmi import give_bmi, apply_limit


def test_cases():
    """Return a list of test cases for give_bmi and apply_limit."""

    asserror = "AssertionError: "
    args_not_lists = asserror + "Both of the arguments must be lists."
    size_error = asserror + "Both of the list must be the same size."
    integer_float_error = asserror + "Elements in both"\
        " of the lists must be integers or floats."
    zero_in_height_error = asserror + "Numbers cannot be 0 in the height list."
    bmi_not_list = asserror + "bmi arg must be a list."
    limit_not_integer = asserror + "limit must be an integer."
    invalid_elements_in_bmi = asserror + "Elements in both of"\
        " the lists must be integers or floats."

    cases = [
        # Normal cases for give_bmi
        {
            "name": "Test 1: Subject case for give_bmi",
            "function": give_bmi,
            "args": ([2.71, 1.15], [165.3, 38.4]),
            "kwargs": {},
            "expected": [22.507863455018317, 29.0359168241966],
            "rel_tol": 1e-15,
        },
        {
            "name": "Test 2: 5 elements (only float) for give_bmi",
            "function": give_bmi,
            "args": ([1.8, 1.7, 1.6, 1.9, 1.5], [72, 65, 60, 90, 50]),
            "kwargs": {},
            "expected": [22.22222222222222,
                         22.49134948096886,
                         23.437499999999996,
                         24.930747922437675,
                         22.22222222222222],
            "rel_tol": 1e-15,
        },
        {
            "name": "Test 3: 7 elements (int and float mixed) for give_bmi",
            "function": give_bmi,
            "args": ([2.0, 1.8, 1.75, 1.6, 1.5, 1.85, 2.1],
                     [100, 80, 75, 65, 55, 90, 110]),
            "kwargs": {},
            "expected": [25.0, 24.691358024691358,
                         24.489795918367346,
                         25.390624999999996,
                         24.444444444444443,
                         26.296566837107375,
                         24.943310657596373],
            "rel_tol": 1e-15,
        },
        {
            "name": "Test 4: Empty lists for give_bmi",
            "function": give_bmi,
            "args": ([], []),
            "kwargs": {},
            "expected": [],
        },
        # Error cases for give_bmi
        {
            "name": "Test 5: Error case (mismatched sizes) for give_bmi",
            "function": give_bmi,
            "args": ([1.8, 1.7], [70]),
            "kwargs": {},
            "expected": size_error,
        },
        {
            "name": "Test 6: Error case (non-numeric values) for give_bmi",
            "function": give_bmi,
            "args": ([1.8, "not a number", 1.7], [72, 65, 60]),
            "kwargs": {},
            "expected": integer_float_error,
        },
        {
            "name": "Test 7: Error case (zeros in height) for give_bmi",
            "function": give_bmi,
            "args": ([1.8, 0, 1.7], [72, 65, 60]),
            "kwargs": {},
            "expected": zero_in_height_error,
        },
        {
            "name": "Test 8: Error case (non-list input) for give_bmi",
            "function": give_bmi,
            "args": ("not a list", [72, 65, 60]),
            "kwargs": {},
            "expected": args_not_lists,
        },
        {
            "name": "Test 9: Error case (mixed valid"
            "and invalid inputs) for give_bmi",
            "function": give_bmi,
            "args": ([1.8, 1.7, [1.6, 1.5]], [72, 65, 60]),
            "kwargs": {},
            "expected": integer_float_error,
        },
        # Normal cases for apply_limit
        {
            "name": "Test 10: Subject case for apply_limit",
            "function": apply_limit,
            "args": ([22.507863455018317, 29.0359168241966], 26),
            "kwargs": {},
            "expected": [False, True],
        },
        # Error cases for apply_limit
        {
            "name": "Test 11: Error case (bmi not a list) for apply_limit",
            "function": apply_limit,
            "args": ("not a list", 25),
            "kwargs": {},
            "expected": bmi_not_list,
        },
        {
            "name": "Test 12: Error case (limit"
            " not an integer) for apply_limit",
            "function": apply_limit,
            "args": ([22.5, 24.0, 26.0], "not an integer"),
            "kwargs": {},
            "expected": limit_not_integer,
        },
        {
            "name": "Test 13: Error case"
            " (bmi contains invalid elements) for apply_limit",
            "function": apply_limit,
            "args": ([22.5, "invalid", 26.0], 25),
            "kwargs": {},
            "expected": invalid_elements_in_bmi,
        },
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
