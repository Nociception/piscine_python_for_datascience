#!/usr/bin/env python3

import sys

def whatis() -> None:
	nb_args = len(sys.argv) - 1
	if nb_args == 0 : exit()
	assert nb_args == 1, ("more than one argument is provided")

	try : arg = int(sys.argv[1])
	except : raise AssertionError("argument must be an integer")

	parity = "Odd" if arg%2 else "Even"
	print(f"I'm {parity}.")

if __name__ == "__main__" :
	try : whatis()
	except AssertionError as error : 
		print(f"{type(error).__name__}: {error}", file=sys.stderr)
