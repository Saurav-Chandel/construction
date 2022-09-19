import datetime
import pytz
import tzlocal
from django.utils import timezone

import time

print(time.ctime())

print(datetime.date.today())


current_local_time=datetime.datetime.now()
print('local time',current_local_time)

current_utc_time=datetime.datetime.utcnow()
print('current utc time',current_utc_time)


local_time_zone=tzlocal.get_localzone()
print(local_time_zone)
print(current_utc_time.replace(tzinfo=pytz.utc).astimezone(local_time_zone))



print(')))))))))))))))))))))')

from datetime import datetime

date_string = "21 June, 2018"

print("date_string =", date_string)
print("type of date_string =", type(date_string))

date_object = datetime.strptime(date_string, "%d %B, %Y")

print("date_object =", date_object)
print("type of date_object =", type(date_object))


print('*&&&&&&&&&&&&&&&&&&&&')
from datetime import datetime

now = datetime.now() # current date and time

year = now.strftime("%Y")
print("year:", year)

month = now.strftime("%m")
print(month)
print("month:",type( month))

day = now.strftime("%d")
print("day:", day)

time = now.strftime("%H:%M:%S")
print("time:", time)

date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
print(date_time)
print("date and time:",type(date_time))	
