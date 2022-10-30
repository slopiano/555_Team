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
        d2 = datetime(int(year), month_dict[month], int(day))
        return True
    except ValueError:
        return False

def thirty_day_ahead(this_date):
    if this_date == 'N/A':
        return False
    d1 = (date.today()+timedelta(days=30))
    d1 = datetime(year=d1.year, month=d1.month, day=d1.day)
    d2 = date.today()
    d2 = datetime(year=d2.year, month=d2.month, day=d2.day)
    curr_year = d2.strftime("%Y")
    curr_year = int(curr_year)
    day, month, year = this_date.split()
    d3 = datetime(curr_year, month_dict[month], int(day))
    curr_year+=1
    d4 = datetime(curr_year, month_dict[month], int(day))
    if (d3 > d2 and d3 < d1) or (d4 > d2 and d4 < d1):
        return True
    else:
        return False
