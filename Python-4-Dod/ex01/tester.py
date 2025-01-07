# Subject
"""
Your tester.py:
from in_out import outer
from in_out import square
from in_out import pow
my_counter = outer(3, square)
print(my_counter())
print(my_counter())
print(my_counter())
print("---")
another_counter = outer(1.5, pow)
print(another_counter())
print(another_counter())
print(another_counter())

Expected output:
$> python tester.py
9
81
6561
---
1.8371173070873836
3.056683336818703
30.42684786675409
$>
"""

from in_out import outer, square, pow

my_counter = outer(3, square)
print(my_counter())
print(my_counter())
print(my_counter())
print("---")
another_counter = outer(1.5, pow)
print(another_counter())
print(another_counter())
print(another_counter())
