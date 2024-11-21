# Subject
"""
Exercice 02: load my image
Turn-in directory : ex02/
Files to turn in : load_image.py
Allowed functions : all libs for load images and table manipulation

You need to write a function that loads an image,
prints its format, and its pixels content in RGB format.
You have to handle, at least, JPG and JPEG format.
You need to handle any error with a clear error message

Here's how it should be prototyped :
def ft_load(path: str) -> array: (you can return to the desired format)
#your code here

Your tester.py:
from load_image import ft_load
print(ft_load("landscape.jpg"))

Expected output:
$> python tester.py
The shape of image is: (257, 450, 3)
[[[19 42 83]
[23 42 84]
[28 43 84]
...
[ 0 0 0]
[ 1 1 1]
[ 1 1 1]]]
$>
"""

import numpy as np
from PIL import Image

def ft_load(path: str) -> np.ndarray:
    """
    Loads an image from the given path, validates its format,
    and returns its pixel data as a NumPy array in RGB format.

    Args:
        path (str): The path to the image file.

    Returns:
        np.ndarray: A 3D NumPy array containing the pixel data of the image.

    Raises:
        AssertionError: If the path is not a string, the file format is unsupported,
                        or the file cannot be opened.
    """

    def parsing(path: str) -> None:
        """Checks if the provided path points to a valid static image file."""

        assert isinstance(path, str), ("Error: path is not a string.")
        
        VALID_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        assert path.lower().endswith(VALID_FORMATS), (
            "Error: unsupported file format.\n"
            f"Supported format are: {', '.join(VALID_FORMATS)}."
        )

        try:
            with open(path, 'rb') as f:
                pass
        except FileNotFoundError:
            raise AssertionError(f"Error: File not found at path '{path}'.")
        except IOError:
            raise AssertionError(
                f"Error: Unable to open the file at '{path}."
            )

    try:
        parsing(path)

    except