# Subject
"""
Your tester.py:
from new_student import Student
student = Student(name = "Edward", surname = "agle")
print(student)
Expected output: (id is random)
$> python tester.py
Student(
    name='Edward',
    surname='agle',
    active=True,
    login='Eagle',
    id='trannxhndgtolvh'
)
$>
10
Training Piscine Python for datascience - 4 Data Oriented Design
The login and id should not be initializable and must return an
error.
Your tester.py:
from new_student import Student
student = Student(name = "Edward", surname = "agle", id = "toto")
print(student)
Expected output:
$> python tester.py
...
TypeError: Student.__init__() got an unexpected keyword argument 'id'
$>
"""

from new_student import Student

student = Student(name="Edward", surname="agle")
print(student)

try:
    student = Student(name="Edward", surname="agle", id="toto")
    print(student)
except TypeError as error:
    print(error)

try:
    student = Student(name="Edward", surname="agle", login="lol")
    print(student)
except TypeError as error:
    print(error)
