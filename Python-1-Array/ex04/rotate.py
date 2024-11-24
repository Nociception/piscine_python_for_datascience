# Subject
"""
Exercice 04: rotate me
Turn-in directory : ex04/
Files to turn in : load_image.py, rotate.py
Allowed functions : all libs for load, manipulate, display image and table
manipulation

Make a program which must load the image "animal.jpeg",
cut a square part from it and transpose it to produce the image below.
It should display it, print the new shape
and the data of the image after the transpose.

Expected output:
$> python rotate.py
The shape of image is: (400, 400, 1) or (400, 400)
[[[167]
[180]
[194]
...
[102]
[104]
[103]]]
New shape after Transpose: (400, 400)
[[167 180 194 ... 64 50 72]
...
[115 116 119 ... 102 104 103]]
$>
Your array after the transpose can be different.
You can look for the transpose method, it could help you ...
You have to do the transpose yourself, no library is allowed for the
transpose

Expected output: see the expected.jpg file in the git hub repo.
"""

import numpy as np
from load_image import ft_load
import matplotlib.pyplot as plt


def manual_transpose(matrix: np.ndarray) -> np.ndarray:
    """
    Manually transposes a 2D or 3D NumPy array.

    Args:
        matrix (np.ndarray): The array to transpose.

    Returns:
        np.ndarray: Transposed array.
    """

    if len(matrix.shape) == 2:  # grayscale
        transposed = np.zeros((matrix.shape[1],
                               matrix.shape[0]),
                              dtype=matrix.dtype)
        # prepares a zero matrix with inverted shapes from the original matrix

        for i in range(matrix.shape[0]):  # lines
            for j in range(matrix.shap[1]):  # columns
                transposed[j][i] = matrix[i][j]
        return transposed

    elif len(matrix.shape) == 3:  # colors
        transposed = np.zeros((matrix.shape[1],
                               matrix.shape[0],
                               matrix.shape[2]),
                              dtype=matrix.dtype)

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                for k in range(matrix.shape[2]):
                    transposed[j][i][k] = matrix[i][j][k]
        return transposed


def rotate(img_path: str,
           x: int,
           y: int,
           size: int,
           grayscale: bool = True) -> None:
    """
    Loads an image, extracts a square region, transposes it manually,
    and optionally converts it to grayscale.

    Args:
        img_path (str): Path to the image file.
        x (int): X-coordinate of the top-left corner of the square region.
        y (int): Y-coordinate of the top-left corner of the square region.
        size (int): Width and height of the square region.
        grayscale (bool): If True, converts the image to grayscale.

    Returns:
        None
    """

    def parsing(img_path, x, y, size, img_array) -> int:
        """
        Validates input parameters and adjusts size if necessary.

        Args:
            img_path (str): Path to the image file.
            x (int): X-coordinate of the top-left corner.
            y (int): Y-coordinate of the top-left corner.
            size (int): Size of the square region.
            img_array (np.ndarray): The loaded image as a NumPy array.

        Returns:
            int: Adjusted size of the square region.

        Raises:
            AssertionError: If parameters are invalid or exceed image bounds.
        """

        assert isinstance(img_path, str), "Image path must be a string."
        assert isinstance(x, int) and isinstance(y, int), (
            "x and y must be integers.")
        assert isinstance(size, int), "Size must be an integer."
        assert x >= 0 and y >= 0, "x and y must be non-negative."
        assert size > 0, "Size must be positive."
        assert x < img_array.shape[1], "x exceeds image width."
        assert y < img_array.shape[0], "y exceeds image height."

        max_size = min(img_array.shape[1] - x, img_array.shape[0] - y)
        adjusted_size = min(size, max_size)

        return adjusted_size

    try:
        img_array = ft_load(img_path)

        print(f"The shape of the image is: {img_array.shape}")
        print(img_array)

        adjusted_size = parsing(img_path, x, y, size, img_array)

        square_region = img_array[y:y + adjusted_size, x:x + adjusted_size]

        if grayscale:
            square_region = np.mean(square_region,
                                    axis=2,
                                    dtype=int,
                                    keepdims=True)

        print(f"New shape after slicing: {square_region.shape}")
        print(square_region)

        transposed = manual_transpose(square_region)

        print(f"New shape after Transpose: {transposed.shape}")
        print(transposed)

        plt.imshow(transposed,
                   cmap="gray" if grayscale else None,
                   interpolation="nearest")
        plt.title("Transposed Image")
        plt.show()

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    rotate(
        img_path="animal.jpeg",
        x=450,
        y=100,
        size=400,
        grayscale=True
    )
