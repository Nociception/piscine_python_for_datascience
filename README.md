# Introduction
This post common core [42](https://42.fr)'s piscine is an intensive program which allows to learn basical and advanced python skills in a data manipulation and analysis context.
Designed with complexity ascending modules, each of them introduces a new concept, more or less one by one. They must be validated in the order they are proposed.

---

# The Modules (also called Days)
## Python - 0 - Starting : basics
### ex00: First python script
Discover python containers (string, list, tuple, set, dict)
### ex01: First use of package
Import and use a package: datetime.
(I plan to use the pendulum package instead, as I heard it is excellent.)
### ex02: First function python
How python types its objects.
### ex03: NULL not found
Different types of python null.
### ex04: The Even and the Odd
Raise an AssertionError.
### ex05: First standalone program python
From now on:
- no code in the global scope
- each program must have its main
- all exceptions must be caught
- all function must have its docstring
- code must be at flake8 norm
I decided to apply these rules on the previous exercises.

Retrieve args from the CLI.
### ex06: filter
Use list comprehensions to imitate filter.
Lambda functions.
### ex07: Dictionaries SoS
Use a dictionnary.
### ex08: Loading ...
Discover the yield python keyword.
### ex09: My first package creation
Exploring the package creation procedure.
Instructive notes in the .sh file.

## Python - 1 - Array : numpy arrays
### ex00: Give my BMI
Discover numpy with 1-dimension arrays.
### ex01: 2D array
Slicing on 2D arrays.
### ex02: load my image
RGB pixel management: manipulating 3D arrays from a picture file.
### ex03: zoom on me
Use slicing on a picture file to zoom on it.
### ex04: rotate me
Transpose a 3D array.
### ex05: Pimp my image
Alter colors in a picture with operations on pixels.

## Python - 2 - DataTable : pandas
### ex00: Load my Dataset
Load a CSV into a pandas's dataframe.
### ex01: draw my country
Plot data from a specific line in a CSV with Matplotlib.
### ex02: compare my country
Plot two lines of a CSV on the same figure, with a specific data crop.
### ex03: draw my year
Merge two CSV to draw a scatter plot on specific common column.
Modify the scale (logarithmic).

This exercise lead to a mini self initiative "project":
[log_vs_lin_scale_on_scatter](github.com/Nociception/log_vs_lin_scale_on_scatter).

## Python - 3 - OOP : for "Object Oriented Programmation"
As this piscine is available only after the 42's common core, I already have studied OOP with common core CPP modules.
### ex00: GOT S1E9
Abstract classes, abstract methods, inheritance.
### ex01: GOT S1E7
.super() method, magic methods (\_\_repr\_\_, \_\_str\_\_), classmethod.
### ex02: Now it’s weird!
Properties, Diamond inheritance in python.
### ex03: Calculate my vector
Operators override.
### ex04: Calculate my dot product
staticmethod

## Python - 4 - DOD : for "Data Oriented Design"
### ex00: Calculate my statistics
Manage an unknown number of parameters with \*\*kwargs.
### ex01: Outer_inner
nonlocal python keyword usage, with a function defined inside a function.
### ex02: my first decorating
Building a decorator from scratch, with the nonlocal keyword, and a function, defined in a function, defined in a function.
### ex03: data class
Discover dataclass decorator.

---

# Tests
The subject provides minimal tests, and encourages us to write better ones.
To do so, I tried to create a tester machine to avoid redundant code:
- [general_function_tester.py](general_function_tester.py) for functions
- [general_tester.py](general_tester.py) for programs

Eventually, I prefered the pytest way.

---

# The piscine concept
Each module must be validated separately in a dedicated repo.
As soon as the repo is locked, we have two days to defend it in front of two students also working on the piscine.
We are encouraged to ask eachother in case of we would be stuck,
and to compare our solutions.
