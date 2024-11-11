#!/usr/bin/env python3

import sys
from ft_filter import ft_filter


def main():
    """Receive two argument from the CLI, in the following order:
    - a string with word(s), space separated,
    (use " for your "string" in the CLI)
    which contains no punction marks character, nor invisible characters
    - an integer, the minimum_length ; no sign, nor .

    Returns the list of words from your string whose length is greater than
    or equal to minimum_length.
    Returns [] if no word fits the condition."""
    DEBUG = 1

    only_error_text = "the arguments are bad"
    args = sys.argv
    text = ""
    length_minimum = -1
    try:
        assert len(args) - 1 == 2, (only_error_text + f"{DEBUG*'(1)'}")

        text = args[1]
        punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        invisible_chars = "\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007"\
            "\u0008\u0009\u000A\u000B\u000C\u000D\u000E\u000F\u0010\u0011"\
            "\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001A\u001B"\
            "\u001C\u001D\u001E\u001F\u007F\u00A0\u2000\u2001\u2002\u2003"\
            "\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u2028\u2029\u202F"\
            "\u205F\u3000"
        if any(c in punctuation + invisible_chars for c in text):
            raise AssertionError(only_error_text + f"{DEBUG*'(2)'}")

        length_minimum = args[2]
        assert int(length_minimum), (only_error_text + f"{DEBUG*'(3)'}")
        assert length_minimum.isdigit(), (only_error_text + f"{DEBUG*'(4)'}")
        length_minimum = int(length_minimum)

        print(list(
            ft_filter(lambda x: len(x) >= length_minimum, text.split())))

    except AssertionError as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
    except Exception:
        print(f"AssertionError: {only_error_text}{DEBUG*'(5)'}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
