def my_decorator(func):
    """DOCSTRING"""

    def wrapper():
        """DOCSTRING"""

        print("Before the function")
        func()
        print("After the function")

    return wrapper


@my_decorator
def hello():
    """DOCSTRING"""

    print("Hello, world!")


def main():
    """DOCSTRING"""

    hello()


if __name__ == "__main__":
    main()
