import subprocess


def general_tester(script_path: str,
                   tests_dict: dict, debug: bool = False) -> None:
    """DOCSTRING"""
    GREEN = "\033[32m"
    RED = "\033[31m"
    DEFAULT_COLOR = "\033[0m"
    debug = 1 if debug else 0

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
            # test_command = ["python3", script_path] + case.split()
            # result = subprocess.run(test_command,
            #                         capture_output=True,
            #                         text=True, encoding="utf-8")
            
            test_command = f"python3 {script_path} {case}"
            result = subprocess.run(test_command, capture_output=True, text=True, shell=True)


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
