import sys


def main():
    """
    Gather many testcases to understand better how does yield work.
    """

    def simple_generator():
        yield 1
        yield 2
        yield 3

    # Not the right way to get what the simple_generator generate
    print("# Print the function (which became a generator)")
    for k in range(3):
        print(simple_generator())
    """
    python3 training_yield.py
    <generator object simple_generator at 0x7f55135b6030>
    <generator object simple_generator at 0x7f55135b6030>
    <generator object simple_generator at 0x7f55135b6030>
    """
    print()

    # The way to get the values
    print("# Getting the generator's value through iterating the function")
    for value in simple_generator():
        print(value)
    """
    python3 training_yield.py
    1
    2
    3
    """
    print()

    # The next() function
    print("# The next() function")
    generator = simple_generator()
    try:
        print(next(generator))
        print(next(generator))
        print(next(generator))
        # One more call next(generator) leads to an error
        print(next(generator))
        print("Unreachable print")
    except StopIteration as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
    """
    python3 training_yield.py
    1
    2
    3
    StopIteration:
    """
    print()

    # Exhaustion of the generators, with affection and for loops
    print("# Exhaustion of the generators, with affection and for loops")
    gen1 = simple_generator()
    try:
        print("Let's iterate gen1 a first time")
        for item in gen1:
            print(item)
        print("First for iterating gen1 DONE\n")
        print("Let's iterate gen1 a second time")
        for item in gen1:
            print(item)
        print("Second for iterating gen1 DONE\n")
        print("A second for iterating an exhausted generator"
              " prints nothing,"
              " and does not raise any StopIteration exception.")
    except StopIteration as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
    gen2 = simple_generator()
    try:
        print("Let's iterate gen2")
        for item in gen2:
            print(item)
        print("for iterating gen2 DONE\n")
        print("End of try bloc, no exception raised")
        print("gen1 and gen2 are two indepedant one-use instances"
              " of simple_generator.")
    except StopIteration as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
    """
    Generator exhaustion and for loops
    Let's iterate gen1 a first time
    1
    2
    3
    First for iterating gen1 DONE

    Let's iterate gen1 a second time
    Second for iterating gen1 DONE

    A second for iterating an exhausted generator prints nothing,
    and does not raise any StopIteration exception.
    Let's iterate gen2
    1
    2
    3
    for iterating gen2 DONE

    End of try bloc, no exception raised
    gen1 and gen2 are two indepedant one-use instances
    of simple_generator.
    """
    print()

    # Repeated for loops on the original generator instance
    print("Repeated for loops on the original generator instance")
    print("Two new for loops on simple_generator():")
    print("First for loop:")
    for item in simple_generator():
        print(item)
    print("First for loop done.")
    print("Second for loop:")
    for item in simple_generator():
        print(item)
    print("Second for loop done.")
    print("These two new for loop print the values :\n"
          "simple_generator original instance"
          " is refilled at each new for loop.")
    """
    First for loop:
    1
    2
    3
    First for loop done.
    Second for loop:
    1
    2
    3
    Second for loop done.
    These two new for loop print the values :
    simple_generator original instance is refilled at each new for loop.
    """
    print()

    # Interactive generators, with the send method
    print("# Interactive generators, with the send method")

    def interactive_generator():
        """
        An interactive generator that accepts and
        yields values dynamically.
        """

        a = yield "First value (starting the generator)"
        b = yield f"Value sent to the interactive_generator : {a}"
        c = yield f"Value sent to the interactive_generator : {b}"
        d = yield f"Value sent to the interactive_generator : {c}"
        e = yield f"Value sent to the interactive_generator : {d}"
        f = yield f"Value sent to the interactive_generator : {e}"
        yield f"Final Result : f={f}"

    gen = interactive_generator()
    print(next(gen))
    print(gen.send(1))
    print(gen.send(2))
    print(gen.send(3))
    print(gen.send(4))
    print(gen.send(5))
    print(gen.send(6))

    print("\nAnother example:")

    def simple_send_example():
        """
        A simple example to demonstrate
        the send method with generators.
        """

        val = yield "Start"
        yield f"Received : {val}"

    gen = simple_send_example()
    print(next(gen))
    print(gen.send("Test"))
    print("The send method sends a value to the last executed yield.\n"
          "If this yield was affected to a variable, the value sent"
          " through the send method is captured.")

    # Countdown
    print("\nCountdown")

    def countdown(n):
        """Generates a countdown from n to 0."""

        while n >= 0:
            yield n
            n -= 1

    for number in countdown(5):
        print(number)

    # Linear progression
    print("\nLinear progression")

    def linear_progression(steps):
        """
        Generates percentages for a linear progression
        in specified steps.
        """

        for i in range(steps + 1):
            yield int((i / steps) * 100)
    for percent in linear_progression(10):
        print(f"Progression: {percent}%")


if __name__ == "__main__":
    main()
