from ft_calculator import calculator
from io import StringIO
import sys


def capture_output(func, *args):
    captured_output = StringIO()
    sys.stdout = captured_output
    func(*args)
    sys.stdout = sys.__stdout__
    return captured_output.getvalue().strip()


def test_dotproduct():
    v1 = [5, 10, 2]
    v2 = [2, 4, 3]
    expected_output = "Dot product is: 56"
    output = capture_output(calculator.dotproduct, v1, v2)
    assert output == expected_output


def test_add_vec():
    v1 = [5, 10, 2]
    v2 = [2, 4, 3]
    expected_output = "Add Vector is: [7.0, 14.0, 5.0]"
    output = capture_output(calculator.add_vec, v1, v2)
    assert output == expected_output


def test_sous_vec():
    v1 = [5, 10, 2]
    v2 = [2, 4, 3]
    expected_output = "Sous Vector is: [3.0, 6.0, -1.0]"
    output = capture_output(calculator.sous_vec, v1, v2)
    assert output == expected_output


def test_edge_cases():
    v1 = []
    v2 = []
    expected_output_dot = "Dot product is: 0"
    output_dot = capture_output(calculator.dotproduct, v1, v2)
    assert output_dot == expected_output_dot

    expected_output_add = "Add Vector is: []"
    output_add = capture_output(calculator.add_vec, v1, v2)
    assert output_add == expected_output_add

    expected_output_sous = "Sous Vector is: []"
    output_sous = capture_output(calculator.sous_vec, v1, v2)
    assert output_sous == expected_output_sous


def test_large_vectors():
    v1 = [1e9, 2e9, 3e9]
    v2 = [1e9, -1e9, 0]
    expected_output_dot = "Dot product is: -1e+18"
    output_dot = capture_output(calculator.dotproduct, v1, v2)
    assert output_dot == expected_output_dot

    expected_add = "Add Vector is: [2000000000.0, 1000000000.0, 3000000000.0]"
    output_add = capture_output(calculator.add_vec, v1, v2)
    assert output_add == expected_add

    expected_output_sous = "Sous Vector is: [0.0, 3000000000.0, 3000000000.0]"
    output_sous = capture_output(calculator.sous_vec, v1, v2)
    assert output_sous == expected_output_sous
