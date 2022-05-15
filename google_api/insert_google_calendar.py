import datetime

from google_token import google_calendar

now = datetime.datetime.now()
now2 = now + datetime.timedelta(hours=1)

print(google_calendar.get_google_token())