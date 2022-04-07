import datetime
import calendar


now = datetime.date.today()
cal = calendar.Calendar()
days = list(cal.itermonthdays2(now.year, now.month))
print(days)