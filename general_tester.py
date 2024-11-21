import subprocess


def general_tester(script_path: str,
                   tests_dict: dict, debug: bool = False) -> None:
    """Receives a tests_dict: {tests_type: ['result expected',
    'test_case1', 'test_case2', ...]}

    Checks if the progam written in the scripth_path file provides
    the same output as expected, for each test_case.

    debug on True for more details.

    Returns nothing.

    Usage:
    In a python script, not in the shell.
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
        general_tester(script_path, tests_dict(), debug)"""

    GREEN = "\033[32m"
    RED = "\033[31m"
    DEFAULT_COLOR = "\033[0m"

    if debug:
        print(f"script_path = {script_path}\n"
              f"tests_dict = {tests_dict}")

    for test_type, cases in tests_dict.items():
        print(f"\n# {test_type} tests :")
        expected = cases[0]
        std = "err" if "Error" in expected else "out"
        if debug:
            print(f"std = {std}")

        for case in cases[1:]:
            if ' ' in case:
                test_command = f'python3 "{script_path}" {case}'
                result = subprocess.run(test_command,
                                        capture_output=True,
                                        text=True,
                                        shell=True)
            else:
                test_command = ["python3", script_path] + case.split()
                result = subprocess.run(test_command,
                                        capture_output=True,
                                        text=True,
                                        shell=False)

            output = result.stdout if std == "out" else result.stderr
            if debug:
                print(f"case = {case} ; output = {output}")
                print(f"Command: {test_command}")
                print(f"stdout: {result.stdout}")
                print(f"stderr: {result.stderr}")

            try:
                assert output.strip() == expected, (
                     f"Test failed for input {case}. "
                     f"Expected: '{expected}', but got: '{output.strip()}'"
                )
                print(f"{GREEN}Test passed for : {case}{DEFAULT_COLOR}")
            except AssertionError as error:
                print(f"{RED}{error}{DEFAULT_COLOR}")
