import sys
from ft_filter import ft_filter


def main(details) -> None:
    """Tests the ft_filter function."""

    GREEN = "\033[32m"
    RED = "\033[31m"
    DEFAULT_COLOR = "\033[0m"

    test_cases = [
        ("None", [0, 1, 2, '', 'hello', None, [], [1, 2], False, True]),
        ("lambda x: x % 2 == 0", [1, 2, 3, 4, 5, 6]),
        ("lambda x: len(x) > 0", ['hello', '', 'world', 'python', '']),
        ("lambda x: x > 0", [-1, 0, 1, 2, -2, 3]),
        ("None", [True, False, True, False]),
        ("lambda x: x > 0", []),
        ("None", [None, None, None]),
        ("lambda x: x.real > 0", [1 + 1j, -1 + 1j, 2 - 2j, -3 - 3j]),
        ("lambda x: 'a' in x",
         ['apple', 'banana', 'cherry', 'date', 'fig', 'grape']),
        ("lambda x: x > 2.5", [1.0, 2.5, 3.0, 4.5, 0.5]),
        ("lambda d: 'key' in d",
         [{'key': 1}, {'other': 2}, {'key': 3, 'value': 4}])
    ]

    def eval_lambda(lambda_str):
        return eval(lambda_str) if lambda_str != "None" else None

    def ft_filter_vs_native_filter(lambda_str, iterable):
        predicate = eval_lambda(lambda_str)
        expected = list(filter(predicate, iterable))
        result = list(ft_filter(predicate, iterable))
        try:
            assert result == expected, (
                f"{RED}Test failed for ({lambda_str}, {iterable})\n"
                f"Expected: {expected}, but got: {result}{DEFAULT_COLOR}"
            )
            print(f"{GREEN}Test passed{DEFAULT_COLOR}")
        except AssertionError as error:
            print(f"{type(error).__name__}: {error}")

    for lambda_str, iterable in test_cases:
        if details:
            print(f"Running test with ({lambda_str}, {iterable})")
        ft_filter_vs_native_filter(lambda_str, iterable)

    def is_prime(n: int) -> bool:
        """Returns True if n is a prime number, False otherwise"""

        if n < 2:
            return False

        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    if details:
        print("predicate=is_prime function ; iterable=list(range(-5, 101))")
    try:
        numbers = list(range(-5, 101))
        result = list(ft_filter(is_prime, numbers))
        expected = list(filter(is_prime, numbers))
        assert result == expected, (
            f"{RED}Test failed for (is_prime, list(range(-5, 101)))\n"
            f"Expected: {expected}, but got: {result}{DEFAULT_COLOR}"
        )
        print(f"{GREEN}Test passed{DEFAULT_COLOR}")
    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")

    print(f"{GREEN}All tests completed.{DEFAULT_COLOR}")


if __name__ == "__main__":
    details = any(arg == "-details" for arg in sys.argv)
    if not details:
        print("Use the -details option for detailed tests:\n"
              "python3 tester_ft_filter.py -details\n")
    main(details)
