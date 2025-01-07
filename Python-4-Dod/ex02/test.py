def my_decorator(func):
    def wrapper():
        print("Avant la fonction")
        func()
        print("Après la fonction")
    return wrapper


@my_decorator
def hello():
    print("Hello, world!")


hello()
