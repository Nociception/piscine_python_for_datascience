import matplotlib.pyplot as plt
from load_image import ft_load
from pimp_image import ft_invert, ft_red, ft_green, ft_blue, ft_grey


def display_image(image, title):
    """
    Displays an image with a title.

    Args:
        image (np.ndarray): The image to display.
        title (str): The title of the display window.

    Returns:
        None
    """

    if image.shape[-1] == 1:
        image = image.squeeze()
        cmap = "gray"
    else:
        cmap = None

    plt.imshow(image, cmap=cmap, interpolation="nearest")
    plt.title(title)
    plt.axis("off")
    plt.show()


def tester():
    """
    Tests all the filter functions and displays the results.
    """

    img_path = "landscape.jpg"
    original = ft_load(img_path)

    print(f"The shape of the image is: {original.shape}")
    print(original)

    filters = {
        "Invert": ft_invert(original),
        "Red": ft_red(original),
        "Green": ft_green(original),
        "Blue": ft_blue(original),
        "Grey": ft_grey(original)
    }

    for name, filtered_image in filters.items():
        print(f"Displaying: {name}")
        display_image(filtered_image, title=name)


if __name__ == "__main__":
    tester()
