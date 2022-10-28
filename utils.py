from datetime import date, timedelta, datetime
from constants import month_dict

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def parseDate(date):
    day, month, year = date.split()
    return datetime(int(year), month_dict[month], int(day))

def isDateLess(d1, d2):
    return d1 < d2

def thirty_day_difference(this_date):
    d1 = (date.today()-timedelta(days=30))
    d1 = datetime(year=d1.year, month=d1.month, day=d1.day)
    day, month, year = this_date.split()
    d2 = datetime(int(year), month_dict[month], int(day))
    if d1 < d2:
        return True
    return False

def isDateValid(thisDate):
    if thisDate == "N/A":
        return True
    day, month, year =  thisDate.split()
    try:
        datetime.datetime(int(year), month_dict[month], int(day))
        return True
    except ValueError:
        return False