import os
import datetime as dt

def time(start_date, end_day):
    """
    Calculate the time
    """
    def num_of_days_in_mon(date): 
        if date.month in [1, 3, 5, 7, 8, 10, 12]:
            day_in_month = 31
        elif date.month in [4, 6, 9, 11]:
            day_in_month = 30
        elif date.month == 2:
            if date.year % 4 == 0:
                day_in_month = 29
        else:
            day_in_month = 28
        return day_in_month
    
    if start_date.year == dt.datetime.now().year:
        frac_mon_1 = (end_day) / num_of_days_in_mon(dt.datetime.now())
        frac_mon_2 = (num_of_days_in_mon(start_date) - start_date.day) / num_of_days_in_mon(start_date)
        num_full_months = (dt.datetime.now().month - 1) - (start_date.month)
        if num_full_months <= 0:
            num_full_months = 0
        time = num_full_months + frac_mon_1 + frac_mon_2
        return time
    else:
        time = (dt.datetime.now().month - 1) + (dt.datetime.now().day / num_of_days_in_mon(dt.datetime.now()))
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

