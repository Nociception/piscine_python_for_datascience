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
        AssertionError: If the path is not a string,
        the file format is unsupported, or the file cannot be opened.
    """

    def parsing(path: str) -> None:
        """Checks if the provided path points to a valid static image file."""

        assert isinstance(path, str), ("path is not a string.")

        VALID_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        assert path.lower().endswith(VALID_FORMATS), (
            "unsupported file format.\n"
            f"Supported format are: {', '.join(VALID_FORMATS)}."
        )

        try:
            with open(path, 'rb'):
                pass
        except FileNotFoundError:
            raise AssertionError(f"File not found at path '{path}'.")
        except IOError:
            raise AssertionError(
                f"Unable to open the file at '{path}."
            )

    try:
        parsing(path)
        with Image.open(path) as img:
            img = img.convert("RGB")
            pixels = np.array(img)
            print(f"The shape of image is: {pixels.shape}")
            return pixels

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}")
        return np.array([])
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
