from datetime import datetime
from constants import month_dict

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def parseDate(date):
    day, month, year = date.split()
    return datetime(int(year), month_dict[month], int(day))

def isDateLess(d1, d2):
    return d1 < d2
