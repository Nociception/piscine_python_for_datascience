import time
from datetime import datetime

# Subject
"""
Exercice 01: First use of package
Turn-in directory : ex01/
Files to turn in : format_ft_time.py
Allowed functions : time, datetime or any other library that allows to
receive the date

Write a script that formats the dates this way,
of course your date will not be mine
as in the example but it must be formatted the same.

Expected output:
$>python format_ft_time.py | cat -e
Seconds since January 1, 1970: 1,666,355,857.3622 or
1.67e+09 in scientific notation$
Oct 21 2022$
$>
"""

seconds_since_epoch_time = time.time()
# print(type(seconds_since_epoch_time)) #a float

print(f"Seconds since January 1, 1970: {seconds_since_epoch_time:,.4f}"
      f" or {seconds_since_epoch_time:.2e} in scientific notation")

today = datetime.now()
# print(today)
print(today.strftime("%b %d %Y"))
