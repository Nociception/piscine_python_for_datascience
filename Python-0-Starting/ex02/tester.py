import sys
from find_ft_type import all_thing_is_obj


def main(more_test: bool = False) -> None:
    """Tests the all_thing_is_obj function.
    Receives an arg (more_test).
    Use the -more option for more tests:"
    "python3 tester.py -more"""

    ft_list = ["Hello", "tata!"]
    ft_tuple = ("Hello", "toto!")
    ft_set = {"Hello", "tutu!"}
    ft_dict = {"Hello": "titi!"}

    all_thing_is_obj(ft_list)
    all_thing_is_obj(ft_tuple)
    all_thing_is_obj(ft_set)
    all_thing_is_obj(ft_dict)
    all_thing_is_obj("Brian")
    all_thing_is_obj("Toto")
    print(all_thing_is_obj(10))

    """
    Expected output:
    $>python tester.py | cat -e
    List : <class 'list'>$
    Tuple : <class 'tuple'>$
    Set : <class 'set'>$
    Dict : <class 'dict'>$
    Brian is in the kitchen : <class 'str'>$
    Toto is in the kitchen : <class 'str'>$
    Type not found$
    42$
    $>
    """

    if more_test:
        print("\n#MORE TESTS")

        print("\n##List tests ; expected: List : <class 'list'>")
        all_thing_is_obj([])
        all_thing_is_obj(["lol"])
        all_thing_is_obj(["hello",
                          "no",
                          True,
                          [],
                          ["an inside list", "one more element", 42],
                          (),
                          ("a tuple", "with one more element", 4.2, {})])

        print("\n##Tuple tests ; expected: Tuple : <class 'tuple'>")
        all_thing_is_obj(ft_tuple)
        all_thing_is_obj(())
        all_thing_is_obj((2, 3))
        all_thing_is_obj((42, 21, 10.5, "string type"))

        print("\n##Set tests ; expected: Set : <class 'set'>")
        all_thing_is_obj(ft_set)
        all_thing_is_obj({})
        # interesting test : {} is ducktyped as a dict, not a set
        all_thing_is_obj(set())
        all_thing_is_obj({"lol"})
        all_thing_is_obj({4, 2})
        all_thing_is_obj({False, True})
        all_thing_is_obj({2, 2, 2, 2, 2, 2, 3, 57})

        print("\n##Dict tests ; expected: Dict : <class 'dict'>")
        all_thing_is_obj(ft_dict)
        all_thing_is_obj({})
        all_thing_is_obj({2: "two", 3: "three", True: False})
        all_thing_is_obj({True: [1, 2, 45],
                          3: "three",
                          False: False,
                          (2, 4): (4, 2),
                          "42": 42})

        print("\n##String tests ; expected: <string value>"
              "is in the kitchen : <class 'str'>")
        all_thing_is_obj("Brian")
        all_thing_is_obj("Toto")
        all_thing_is_obj("")
        all_thing_is_obj('')
        all_thing_is_obj("lolilol lmfao")

        print("\n##'Type not found' tests ; expected: Type not found")
        print("###Int tests")
        all_thing_is_obj(10)
        all_thing_is_obj(-10)

        print("\n###Float tests")
        all_thing_is_obj(10.5)
        all_thing_is_obj(-10.5)

        print("\n###Function tests ; extra expected: 42")
        print(all_thing_is_obj(10))
        def foo() -> int: return 0
        print(all_thing_is_obj(foo))
        def bar(x: int) -> int: return 24
        print(all_thing_is_obj(bar(42)))


if __name__ == "__main__":
    more_tests = any(arg == "-more" for arg in sys.argv)
    if not more_tests:
        print("Use the -more option for more tests:\n"
              "python3 tester.py -more\n")
    main(more_tests)
