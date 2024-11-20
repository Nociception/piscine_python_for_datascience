from give_bmi import give_bmi, apply_limit
import sys
import io
import math


def tester() -> None:
    """Tests both of the functions give_bmi and apply_limit,
    with normal cases and error cases.

    Returns: nothing."""

    DETAILS = 1

    GREEN = "\033[32m"
    RED = "\033[31m"
    DEFAULT_COLOR = "\033[0m"

    # Normal cases
    def normal_cases_tester(
            height: list,
            weight: list,
            limit: int,
            expected_bmi: list,
            expected_limit: list,
            details: int) -> None:
        """Tests both of the functions give_bmi and apply limits,
        with normal cases, which are not supposed to lauch any error.
        Compares what results both of the functions provide
        with the expected results for each function.

        Args:
            - height: a list of integer/float
            - weight: a list of integer/float
            - limit: an integer
            - expected_bmi : a list of integer/float
            - expected_limit: a list of boolean
            - details: an integer for enable or not details displaying

        Returns: nothing.
        """

        rel_tol = 1e-15

        try:
            if details:
                print("Test values:\n"
                      f"height={height}\n"
                      f"weight={weight}\n"
                      f"limit={limit}\n"
                      f"expected_bmi={expected_bmi}\n"
                      f"expected_limit={expected_limit}\n")

            result_bmi = give_bmi(height, weight)
            if details:
                print(f"give_bmi results: {result_bmi}")

            assert len(result_bmi) == len(expected_bmi), (
                f"Expected length {len(expected_bmi)}, "
                f"but got {len(result_bmi)}"
            )

            for rb, eb in zip(result_bmi, expected_bmi):
                assert math.isclose(rb, eb, rel_tol=rel_tol), (
                    f"Expected {eb}, but got {rb} (tolerance={rel_tol})"
                )

            result_limit = apply_limit(result_bmi, limit)
            if details:
                print(f"apply_limit_result results: {result_limit}")
            assert result_limit == expected_limit, (
                f"Expected {expected_limit}, but got {result_limit}"
            )

            print(f"{GREEN}Test passed.{DEFAULT_COLOR}")

        except AssertionError as error:
            print(f"{RED}{type(error).__name__}: {error}{DEFAULT_COLOR}",
                  file=sys.stderr)

    if True:
        print("\nTest 1: Subject case")
        height = [2.71, 1.15]
        weight = [165.3, 38.4]
        limit = 26
        expected_bmi = [22.507863455018317, 29.0359168241966]
        expected_limit = [False, True]
        normal_cases_tester(
            height, weight, limit, expected_bmi,
            expected_limit, DETAILS)

    if True:
        print("\nTest 2: 5 elements (only float)")
        height = [1.8, 1.7, 1.6, 1.9, 1.5]
        weight = [72, 65, 60, 90, 50]
        limit = 25
        expected_bmi = [22.22222222222222,
                        22.49134948096886,
                        23.437499999999996,
                        24.930747922437675,
                        22.22222222222222]
        expected_limit = [False, False, False, False, False]
        normal_cases_tester(
            height, weight, limit, expected_bmi,
            expected_limit, DETAILS)

    if True:
        print("\nTest 3: 7 elements (int and float mixed)")
        height = [2.0, 1.8, 1.75, 1.6, 1.5, 1.85, 2.1]
        weight = [100, 80, 75, 65, 55, 90, 110]
        limit = 24
        expected_bmi = [25.0, 24.691358024691358,
                        24.489795918367346,
                        25.390624999999996,
                        24.444444444444443,
                        26.296566837107375,
                        24.943310657596373]
        expected_limit = [True, True, True, True, True, True, True]
        normal_cases_tester(
            height, weight, limit, expected_bmi,
            expected_limit, DETAILS)

    if True:
        print("\nTest 4: Empy list")
        height = []
        weight = []
        limit = 25
        expected_bmi = []
        expected_limit = []
        normal_cases_tester(
            height, weight, limit, expected_bmi,
            expected_limit, DETAILS)

    # give_bmi error cases
    asserror = "AssertionError: "
    args_not_lists = asserror + "Both of the arguments must be lists.\n"
    size_error_text = asserror + "Both of the list must be "\
        "the same size.\n"
    integer_float_error_text = asserror + "Elements in both of "\
        "the lists must be integers or floats.\n"
    zero_in_height_error_text = asserror + "Numbers cannot be 0 "\
        "in the height list.\n"

    def capture_stdout(f: object, *args, **kwargs) -> str:
        """
        Captures stdout during a function call.

        Args:
            - *args captures in a tuple every positional arguments
            (in the order they are supposed to be) passed to the function f.
            func(arg1, arg2, arg3) ; args are positionnal here.
            - **kwargs (for keyword arguments) captures in a dictionary
            every named arguments passed to the function.
            func(argA='a', argL='l') ; args are named here (no order needed).

        Returns: a string, with what f has output on the standard output.
        """

        stdout = io.StringIO()  # creates the variable for storing an output.

        old_stdout = sys.stdout
        # old_stdout stores the old reference to the standard output, in order
        # to be able to restore it, letting the program intact.

        try:
            sys.stdout = stdout  # The standard output is now redirected
            # to the variable created at the beginning.

            f(*args, **kwargs)  # f will now print into the variable stdout.
            # The stars here have not the same role as above
            # (in the function def line; see in the docstring).
            # Here, they unpack the tuple and the dictionary into
            # the args section of the f function call.

        except TypeError as error:
            print(f"{RED}{type(error).__name__}: {error}{DEFAULT_COLOR}",
                  file=sys.stderr)

        finally:  # A keyword (in a try bloc) for instructions
            # which will be run anyway without
            # any exit, return or error before.

            sys.stdout = old_stdout  # Then the standard output is restored.

        return stdout.getvalue()  # Returns as a string
        # what the function output.

    def error_cases_give_bmi_tester(
            height: list,
            weight: list,
            expected_error_text: str,
            details: int) -> None:
        """Tests the give_bmi function, with error cases,
        which are supposed to lauch error.
        Compares what error does the give_bmi functions lauches
        with the expected error text.

        Args:
            - height: a list of integer/float
            - weight: a list of integer/float
            - details: an integer for enable or not details displaying

        Returns: nothing.
        """

        if details:
            print("Test values:\n"
                  f"height={height}\n"
                  f"weight={weight}\n"
                  f"expected_error_text={expected_error_text}\n")

        output = capture_stdout(give_bmi, height, weight)

        try:
            assert output == expected_error_text, (
                f"Expected \n{expected_error_text}\nbut got \n{output}"
            )
            print(f"{GREEN}Test passed.{DEFAULT_COLOR}")

        except AssertionError as error:
            print(f"{RED}{type(error).__name__}: {error}{DEFAULT_COLOR}",
                  file=sys.stderr)

    if True:
        print("\nTest 5: Error case: mismatched sized")
        height = [1.8, 1.7]
        weight = [70]
        t = size_error_text
        error_cases_give_bmi_tester(height, weight, t, DETAILS)

    if True:
        print("\nTest 6: Error case: Non-numeric values")
        height = [1.8, "not a number", 1.7]
        weight = [70, 75, 80]
        t = integer_float_error_text
        error_cases_give_bmi_tester(height, weight, t, DETAILS)

    if True:
        print("\nTest 7: Error case: Zero values in height")
        height = [1.8, 0, 1.7]
        weight = [70, 75, 80]
        t = zero_in_height_error_text
        error_cases_give_bmi_tester(height, weight, t, DETAILS)

    if True:
        print("\nTest 8: Error case: Different-sized lists")
        height = [1.8, 1.7]
        weight = [70, 75, 80]
        t = size_error_text
        error_cases_give_bmi_tester(height, weight, t, DETAILS)

    if True:
        print("\nTest 9: Error case: Non-list input")
        height = "not a list"
        weight = [70, 75, 80]
        t = args_not_lists
        error_cases_give_bmi_tester(height, weight, t, DETAILS)

    if True:
        print("\nTest 10: Error case: Mixed valid and invalid inputs")
        height = [1.8, 1.7, [1.6, 1.5]]
        weight = [70, 75, 80]
        t = integer_float_error_text
        error_cases_give_bmi_tester(height, weight, t, DETAILS)

    def error_cases_apply_limit_tester(
            bmi: list[int | float],
            limit: int,
            expected_error_text: str,
            details: int) -> None:
        """Tests the apply_limit function, with error cases,
        which are supposed to launch errors.
        Compares what error does the apply_limit function launches
        with the expected error text.

        Args:
            - bmi: a list of integer/float
            - limit: an integer
            - expected_error_text: the expected error message
            - details: an integer for enabling or not details displaying

        Returns: nothing.
        """

        if details:
            print("Test values:\n"
                  f"bmi={bmi}\n"
                  f"limit={limit}\n"
                  f"expected_error_text={expected_error_text}\n")

        output = capture_stdout(apply_limit, bmi, limit)

        try:
            assert output == expected_error_text, (
                f"Expected \n{expected_error_text}\nbut got \n{output}"
            )
            print(f"{GREEN}Test passed.{DEFAULT_COLOR}")

        except AssertionError as error:
            print(f"{RED}{type(error).__name__}: {error}{DEFAULT_COLOR}",
                  file=sys.stderr)

    # apply_limit error cases
    bmi_not_list = asserror + "bmi arg must be a list.\n"
    limit_not_integer = asserror + "limit must be an integer.\n"
    invalid_elements_in_bmi = asserror + "Elements in both of the"\
        " lists must be integers or floats.\n"

    if True:
        print("\nTest 11: Error case: bmi is not a list")
        bmi = "not a list"
        limit = 25
        error_cases_apply_limit_tester(bmi, limit, bmi_not_list, DETAILS)

    if True:
        print("\nTest 12: Error case: limit is not an integer")
        bmi = [22.5, 24.0, 26.0]
        limit = "not an integer"
        error_cases_apply_limit_tester(bmi, limit, limit_not_integer, DETAILS)

    if True:
        print("\nTest 13: Error case: bmi contains invalid elements")
        bmi = [22.5, "invalid", 26.0]
        limit = 25
        error_cases_apply_limit_tester(
            bmi, limit, invalid_elements_in_bmi, DETAILS)


if __name__ == "__main__":
    tester()
