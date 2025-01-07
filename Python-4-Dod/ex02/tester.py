# Subject
"""
Your tester.py:
from callLimit import callLimit
@callLimit(3)
def f():
print ("f()")
@callLimit(1)
def g():
print ("g()")
for i in range(3):
f()
g()
8
Training Piscine Python for datascience - 4 Data Oriented Design
Expected output:
$> python tester.py
f()
g()
f()
Error: <function g at 0x7fabdc243ee0> call too many times
f()
Error: <function g at 0x7fabdc243ee0> call too many times
$>
"""

from callLimit import callLimit


@callLimit(3)
def f():
    print("f()")


@callLimit(1)
def g():
    print("g()")


for i in range(3):
    f()
    g()
