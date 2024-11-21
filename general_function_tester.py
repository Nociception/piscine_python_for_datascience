import io
import sys
import traceback
import math


def capture_function_output(func, *args, **kwargs):
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

    stdout = io.StringIO()  # creates a variable for storing an output.
    stderr = io.StringIO()  # creates another one.

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    # old_stdout stores the old reference to the standard output, in order
    # to be able to restore it, letting the program intact.
    # same for old_stderr with sys.stderr

    sys.stdout = stdout
    sys.stderr = stderr
    # The standard output is now redirected
    # to the variable created at the beginning.
    # same for the standard error output.

    result, error = None, None

    try:
        result = func(*args, **kwargs)
    except Exception:
        error = traceback.format_exc().strip()
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    return result, stdout.getvalue().strip(), stderr.getvalue().strip(), error


def general_function_tester(test_cases, debug=False, use_error_output=False):
    """Tests a list of functions based on the provided test cases.

    Args:
        test_cases (list): List of dictionaries describing test cases.
        debug (bool): Whether to enable debug output.
        use_error_output (bool): Whether to test error cases using stderr.

    Returns:
        None
    """
    GREEN = "\033[32m"
    RED = "\033[31m"
    DEFAULT_COLOR = "\033[0m"

    for case in test_cases:
        name = case["name"]
        func = case["function"]
        args = case["args"]
        kwargs = case["kwargs"]
        expected = case["expected"]
        rel_tol = case.get("rel_tol", None)

        if debug:
            print(f"\nRunning test: {name}"
                  f"Function: {func.__name__}"
                  f"Args: {args}, Kwargs: {kwargs}"
                  f"Expected: {expected}"
                  f"Relative Tolerance: {rel_tol}")

        result, stdout, stderr, error = capture_function_output(
            func, *args, **kwargs
        )

        if isinstance(expected, str) and "AssertionError:" in expected:
            output_to_compare = stderr if use_error_output else stdout
            passed = output_to_compare == expected
        elif (
            rel_tol is not None
            and isinstance(result, list)
            and isinstance(expected, list)
        ):
            passed = (
                len(result) == len(expected) and
                all(
                    math.isclose(res, exp, rel_tol=rel_tol)
                    for res, exp in zip(result, expected)
                )
            )
        else:
            passed = result == expected

        if passed:
            print(f"{GREEN}Test passed: {name}{DEFAULT_COLOR}")
        else:
            print(f"{RED}Test failed: {name}{DEFAULT_COLOR}")
            if debug:
                print(f"Result: {result}\n"
                      f"Stdout: {stdout}\n"
                      f"Stderr: {stderr}\n"
                      f"Error Traceback: {error}")
                if (
                    rel_tol is not None
                    and isinstance(result, list)
                    and isinstance(expected, list)
                ):
                    print("Detailed Comparison:")
                    for res, exp in zip(result, expected):
                        print(f"Value: {res}, Expected: {exp}, Close: "
                              f"{math.isclose(res, exp, rel_tol=rel_tol)}")
