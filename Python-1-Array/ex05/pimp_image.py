# Subject
"""
Exercice 05: Pimp my image
Turn-in directory : ex05/
Files to turn in : load_image.py, pimp_image.py
Allowed functions : all libs for load, manipulate, display image and table
manipulation

You need to develop 5 functions capable of applying
a variety of color filters to images, while keeping the image shape the same.

Here's how they should be prototyped :
def ft_invert(array) -> array:
#your code here
def ft_red(array) -> array:
#your code here
def ft_green(array) -> array:
#your code here
def ft_blue(array) -> array:
#your code here
def ft_grey(array) -> array:
#your code here

You have some restriction operators for each function:
(you can only use those given, you don't have to use them all)
• invert: =, +, -, *
• red: =, *
• green: =, -
• blue: =
• grey: =, /

Your tester.py:
from load_image import ft_load
from pimp_image import ft_invert
...
array = ft_load("landscape.jpg")
ft_invert(array)
ft_red(array)
ft_green(array)
ft_blue(array)
ft_grey(array)
print(ft_invert.__doc__)

Expected output: (docstrings can be different)
$> python tester.py
The shape of image is: (257, 450, 3)
[[[19 42 83]
[23 42 84]
[28 43 84]
...
[ 0 0 0]
[ 1 1 1]
[ 1 1 1]]]
...
Inverts the color of the image received.
$>

Expected: see the expected_image files in te github repo.
"""

import numpy as np


def ft_invert(array: np.ndarray) -> np.ndarray:
    """
    Inverts the colors of the input image.

    Args:
        array (np.ndarray): The input image array.

    Returns:
        np.ndarray: The inverted image array.
    """

    max_value = 255
    inverted = max_value - array
    """
    This last creates a numpy_array,
    same array's (the function's arg) shape,
    where all elements are 255 - current_element.
    Magic, and quite useful and quick (to read and run).
    """

    return inverted


def ft_red(array: np.ndarray) -> np.ndarray:
    """
    Applies a red filter to the input image.

    Args:
        array (np.ndarray): The input image array.

    Returns:
        np.ndarray: The red-filtered image array.
    """

    red_filtered = array.copy()
    red_filtered[:, :, 1] = 0
    red_filtered[:, :, 2] = 0

    return red_filtered


def ft_green(array: np.ndarray) -> np.ndarray:
    """
    Applies a green filter to the input image.

    Args:
        array (np.ndarray): The input image array.

    Returns:
        np.ndarray: The green-filtered image array.
    """

    green_filtered = array.copy()
    green_filtered[:, :, 0] = 0
    green_filtered[:, :, 2] = 0

    return green_filtered


def ft_blue(array: np.ndarray) -> np.ndarray:
    """
    Applies a blue filter to the input image.

    Args:
        array (np.ndarray): The input image array.

    Returns:
        np.ndarray: The blue-filtered image array.
    """

    blue_filtered = array.copy()
    blue_filtered[:, :, 0] = 0
    blue_filtered[:, :, 1] = 0

    return blue_filtered


def ft_grey(array: np.ndarray) -> np.ndarray:
    """
    Converts an image to grayscale using
    the green channel for all RGB channels. SORCERY !
    Green contributes to 58% of brightness perceived from humain eyes.
    By replicating the green value on the two other channels,
    image appears grayscaled.

    Args:
        array (np.ndarray): The input image array.

    Returns:
        np.ndarray: The grayscale image array.
    """

    height, width, channels = array.shape

    grayscale = np.zeros((height, width, channels), dtype=array.dtype)

    for line in range(height):
        for column in range(width):
            green_value = array[line, column, 1]

            grayscale[line, column] = [green_value, green_value, green_value]

    return grayscale
