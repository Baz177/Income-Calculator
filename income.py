import os
import datetime as dt

def time(start_date):
    """
    Calculate the time
    """
    if dt.datetime.now().month in [1, 3, 5, 7, 8, 10, 12]:
        day_in_month = 31
    elif dt.datetime.now().month in [4, 6, 9, 11]:
        day_in_month = 30
    elif dt.datetime.now().month == 2:
        if dt.datetime.now().year % 4 == 0:
            day_in_month = 29
        else:
            day_in_month = 28
    if start_date.year == dt.datetime.now().year:
        frac_mon_1 = (dt.datetime.now().day) / day_in_month
        frac_mon_2 = (day_in_month - start_date.day) / day_in_month
        num_full_months = (dt.datetime.now().month - 1) - (start_date.month)
        if num_full_months <= 0:
            num_full_months = 0
        time = num_full_months + frac_mon_1 + frac_mon_2
        return time
    else:
        time = (dt.datetime.now().month - 1) + (dt.datetime.now().day / day_in_month)
        return time
    

def gmi_w2(income_type = None, year_to_date = None, rate = None, hours_week=None, start_date=None, time = None):
    """
    Calculate the Gross Monthly Income (GMI) based on the income type and rate.
    """
    if income_type == 'hourly': 
        income = rate * hours_week * 4
    elif income_type == 'weekly':
        income = rate * 4
    elif income_type == 'biweekly':
        income = rate * 2
    elif income_type == 'monthly':
        income = rate 
    elif income_type == 'annual':
        income = rate / 12
    elif income_type == 'daily':
        income = rate * 20
    elif income_type == 'year_to_date':
        income = year_to_date / time 
    print(f'Income: {income}')
    return income

