import sys
from NULL_not_found import NULL_not_found


def main(more_test: bool = False) -> None:
    """
    Tests the NULL_not_found function.
    Receives an arg (more_test).
    Use the -more option for more tests:"
    "python3 tester.py -more
    """

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

    """
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
    """

    if more_test:
        print("\n#MORE TESTS")

        print("\n##Nothing test ; expected: Nothing: None <class 'NoneType'>")
        NULL_not_found(Nothing)

        print("\n##nan tests ; expected: Cheese: nan <class 'float'>")
        NULL_not_found(Garlic)
        NULL_not_found(float("nan"))  # also works
        NULL_not_found(float("NAN"))  # also works
        # NULL_not_found(float("lol")) #does not work
        # NULL_not_found(float("")) #does not work

        print("\n##float(floatable_string) tests ; expected: Type not found")
        NULL_not_found(float("3"))  # Type not found, of course
        NULL_not_found(float("42.0"))  # Type not found, of course

        print("\n##0 tests ; expected: Zero: 0 <class 'int'>")
        NULL_not_found(Zero)
        NULL_not_found(-0)

        print("\n##0.0 tests ; expected: Type not found")
        NULL_not_found(0.0)
        NULL_not_found(-0.0)

        print("\n##Empty tests ; expected: Empty: <class 'str'>\n"
              "with only one space bewteen Empty: and <class 'str'>")
        NULL_not_found(Empty)
        NULL_not_found("")

        print("\n##False test ; expected: Fake: False <class 'bool'>")
        NULL_not_found(Fake)


if __name__ == "__main__":
    more_tests = any(arg == "-more" for arg in sys.argv)
    if not more_tests:
        print("Use the -more option for more tests:\n"
              "python3 tester.py -more\n")
    main(more_tests)
