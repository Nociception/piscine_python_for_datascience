# Subject
"""
Exercice 03: zoom on me
Turn-in directory : ex03/
Files to turn in : load_image.py, zoom.py
Allowed functions : all libs for load, manipulate,
display image and table manipulation

Create a program that should load the image "animal.jpeg",
print some information about it and display it after "zooming".
• The size in pixel on both X and Y axis
• The number of channel
• The pixel content of the image.
• Display the scale on the x and y axis on the image
If anything went wrong, the program must
not stop abruptly and handle any error with a clear message.

Expected output:
$> python zoom.py
The shape of image is: (768, 1024, 3)
[[[120 111 132]
[139 130 151]
[155 146 167]
...
[120 156 94]
[119 154 90]
[118 153 89]]]
New shape after slicing: (400, 400, 1) or (400, 400)
[[[167]
[180]
[194]
...
[102]
[104]
[103]]]
$>

Expected output: See the expected.jpg file in the github repo.
"""

import numpy as np
from load_image import ft_load
import matplotlib.pyplot as plt


def zoom(img_path: str,
         x: int,
         y: int,
         width: int,
         height: int,
         grayscale: bool = True):
    """
    Loads an image, zooms into a defined region,
    and optionally converts it to grayscale.

    Args:
        img_path (str): Path to the image file.
        x (int): X-coordinate of the top-left corner of the zoom region.
        y (int): Y-coordinate of the top-left corner of the zoom region.
        width (int): Width of the zoom region.
        height (int): Height of the zoom region.
        grayscale (bool): If True, converts the image to grayscale.

    Returns:
        None
    """

    def parsing(img_path, x, y, width, height, img_array):
        """
        Validates the input parameters and
        adjusts the zoom dimensions if necessary.

        Args:
            img_path (str): Path to the image file.
            x (int): X-coordinate of the top-left corner of the zoom region.
            y (int): Y-coordinate of the top-left corner of the zoom region.
            width (int): Width of the zoom region.
            height (int): Height of the zoom region.
            img_array (np.ndarray): The loaded image as a NumPy array.

        Returns:
            tuple: Adjusted width and height of the zoom region.

        Raises:
            AssertionError: If the parameters are invalid
            or exceed the image bounds.
        """

        assert isinstance(img_path, str), (
            "Image path must be a string.")
        assert isinstance(x, int) and isinstance(y, int), (
            "x and y must be integers.")
        assert isinstance(width, int) and isinstance(height, int), (
            "width and height must be integers.")
        assert x >= 0 and y >= 0, (
            "x and y must be non-negative.")
        assert width > 0 and height > 0, (
            "width and height must be positive.")
        assert x < img_array.shape[1], (
            "x exceeds image dimensions.")
        assert y < img_array.shape[0], (
            "y exceeds image dimensions.")

        max_width = img_array.shape[1]
        max_height = img_array.shape[0]
        adjusted_width = min(width, max_width - x)
        adjusted_height = min(height, max_height - y)

        return adjusted_width, adjusted_height

    try:
        img_array = ft_load(img_path)

        adjusted_width, adjusted_height = parsing(img_path,
                                                  x,
                                                  y,
                                                  width,
                                                  height,
                                                  img_array)

        print(f"The shape of the image is: {img_array.shape}")
        print(img_array)

        if grayscale:
            img_array = np.mean(img_array, axis=2, dtype=int, keepdims=True)
            # dtype=int converts means into integers
            # keepdims=True does not change the matrix shape

        zoomed = img_array[y:y + adjusted_height, x:x + adjusted_width]
        print(f"New shape after slicing: {zoomed.shape}")
        print(zoomed)

        plt.imshow(zoomed.squeeze(),
                   cmap="gray" if grayscale else None,
                   interpolation="nearest")
        # This matplotlib does not show the image, but prepares it,
        # with many parameters
        # zoomed.squeeze() deletes dimension size 1.
        # If there is no such a dimension, no effect.
        # For exemple, with no grayscale : no effect.
        # But with grayscale : the dimension shift from 3 to 2.
        # cmap="gray" uses the gray color for the image rendering
        # Without this parameters, the RGB system is used.
        # interpolation="nearest" leads to the least image alteration

        plt.title("Zoomed Image")

        plt.show()

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    zoom(
        img_path="animal.jpeg",
        x=450,
        y=100,
        width=400,
        height=400,
        grayscale=True
    )
