import time
from datetime import datetime

"""
Write a script that formats the dates this way, of course your date will not be mine
as in the example but it must be formatted the same
"""

seconds_since_epoch_time = time.time()
#print(type(seconds_since_epoch_time)) #a float

print(f"Seconds since January 1, 1970: {seconds_since_epoch_time:,.4f}"
	  f" or {seconds_since_epoch_time:.2e} in scientific notation")

today = datetime.now()
#print(today)
print(today.strftime("%b %d %Y"))