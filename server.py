from flask import Flask, request, render_template, jsonify
from income import gmi_w2, gmi_1099, time as calculate_time
from datetime import datetime
import os
import socket

app = Flask(__name__)

# Define custom Jinja filter for currency formatting
def format_currency(value):
    try:
        return "{:.2f}".format(float(value))
    except (ValueError, TypeError):
        return "Invalid"

app.jinja_env.filters['format_currency'] = format_currency

@app.route('/')
@app.route('/index')
def index():
    print("Accessing /index route")
    return render_template('index.html')

@app.route('/w2-income', methods=['GET'])
def w2_income():
    print("Accessing /w2-income route")
    return render_template('w2-income.html')

@app.route('/1099-income', methods=['GET'])
def income_1099():
    print("Accessing /1099-income route")
    return render_template('three-month-income.html')

@app.route('/year-to-date', methods=['GET', 'POST'])
def year_to_date():
    print("Entering /year-to-date route")
    if request.method == 'GET':
        print("Handling GET request")
        return render_template('year-to-date.html')
    
    print("Handling POST request")
    # Handle both form data and JSON
    if request.is_json:
        data = request.get_json()
        print("Received JSON data:", data)
    else:
        data = request.form.to_dict()
        print("Received form data:", data)
        # Convert string values to appropriate types
        data = {
            'ytdIncome': data.get('ytdIncome'),
            'year': data.get('year'),
            'month': data.get('month'),
            'day': data.get('day')
        }

    if not data or not data.get('ytdIncome'):
        print("No valid data provided")
        return render_template('gmi.html', error='No data provided')

    if data.get('ytdIncome') == 'no':
        print("YTD income is 'no', rendering w2-details.html")
        result = {
            'start_date': f"{data.get('year')}-{data.get('month'):02d}-{data.get('day'):02d}" if data.get('year') and data.get('month') and data.get('day') else 'Not provided',
            'ytd_income': 'no',
            'message': 'No YTD income provided'
        }
        return render_template('w2-details.html', result=result)

    try:
        year = int(data.get('year')) if data.get('year') else None
        month = int(data.get('month')) if data.get('month') else None
        day = int(data.get('day')) if data.get('day') else None
        ytd_income = float(data.get('ytdIncome'))
        print("Parsed data:", year, month, day, ytd_income)

        if year and month and day:
            try:
                start_date = datetime(year, month, day)
                if not (1900 <= year <= 2099):
                    print("Invalid year range")
                    return render_template('gmi.html', error='Year must be between 1900 and 2099')
            except ValueError:
                print("Invalid date")
                return render_template('gmi.html', error='Invalid date')
        else:
            start_date = None

        if ytd_income < 0:
            print("Negative YTD income")
            return render_template('gmi.html', error='YTD income cannot be negative')

        print("Type of gmi_w2:", type(gmi_w2))
        if not callable(gmi_w2):
            print("Error: gmi_w2 is not a function")
            return render_template('gmi.html', error='Internal error: GMI calculation function is invalid')

        time = calculate_time(start_date)
        print("Calculated time:", time)
        gmi = gmi_w2(income_type='year_to_date', year_to_date=ytd_income, start_date=start_date, time=time)
        print("Calculated GMI:", gmi)

        result = {
            'start_date': start_date.strftime('%Y-%m-%d') if start_date else 'Not provided',
            'ytd_income': ytd_income,
            'gmi': gmi,
            'message': "This is the customer's Gross Monthly Income calculated"
        }
        print("Rendering gmi.html with result:", result)
        return render_template('gmi.html', result=result)
    
    except (ValueError, TypeError) as e:
        print(f"Error in POST: {e}")
        return render_template('gmi.html', error=f'Invalid data format: {str(e)}')

@app.route('/w2-details', methods=['GET', 'POST'])
def w2_details():
    print("Accessing /w2-details route")
    if request.method == 'GET':
        try:
            year = int(request.args.get('year')) if request.args.get('year') else None
            month = int(request.args.get('month')) if request.args.get('month') else None
            day = int(request.args.get('day')) if request.args.get('day') else None
            start_date = f"{year}-{month:02d}-{day:02d}" if year and month and day else 'Not provided'
        except (ValueError, TypeError) as e:
            print(f"Error formatting start_date: {e}")
            start_date = 'Invalid date'
        result = {
            'start_date': start_date,
            'ytd_income': 'no',
            'message': 'No YTD income provided, please specify income details'
        }
        print("Rendering w2-details.html with result:", result)
        return render_template('w2-details.html', result=result)
    
    # Handle POST from w2-details.html form
    print("Handling POST request")
    data = request.form.to_dict()
    print("Received form data:", data)

    if not data or not data.get('incomeType'):
        print("No valid data provided")
        return render_template('gmi.html', error='No income type provided')

    try:
        income_type = data.get('incomeType')
        year = int(data.get('year')) if data.get('year') else None
        month = int(data.get('month')) if data.get('month') else None
        day = int(data.get('day')) if data.get('day') else None
        start_date = None
        if year and month and day:
            try:
                start_date = datetime(year, month, day)
                if not (1900 <= year <= 2099):
                    print("Invalid year range")
                    return render_template('gmi.html', error='Year must be between 1900 and 2099')
            except ValueError:
                print("Invalid date")
                return render_template('gmi.html', error='Invalid date')

        # Initialize result dictionary
        result = {
            'start_date': start_date.strftime('%Y-%m-%d') if start_date else 'Not provided',
            'income_type': income_type,
            'rate': 0,
            'hours_per_week': None,
            'ytd_income': 0,
            'gmi': 0,
            'message': f"Gross Monthly Income calculated based on {income_type} rate"
        }
        # Placeholder GMI calculation
        if income_type == 'hourly':
            hourly_rate = float(data.get('hourlyRate', 0))
            hours_per_week = float(data.get('hoursPerWeek', 0))
            if hourly_rate <= 0 or hours_per_week <= 0:
                print("Invalid hourly inputs")
                return render_template('gmi.html', error='Hourly rate and hours per week must be positive')
            result['rate'] = hourly_rate
            result['hours_per_week'] = hours_per_week
            result['ytd_income'] = hourly_rate * hours_per_week * 52  # Annual equivalent
            result['gmi'] = result['ytd_income'] / 12
        elif income_type == 'weekly':
            weekly_rate = float(data.get('weeklyRate', 0))
            if weekly_rate <= 0:
                print("Invalid weekly rate")
                return render_template('gmi.html', error='Weekly rate must be positive')
            result['rate'] = weekly_rate
            result['ytd_income'] = weekly_rate * 52
            result['gmi'] = result['ytd_income'] / 12
        elif income_type == 'biweekly':
            biweekly_rate = float(data.get('biweeklyRate', 0))
            if biweekly_rate <= 0:
                print("Invalid biweekly rate")
                return render_template('gmi.html', error='Biweekly rate must be positive')
            result['rate'] = biweekly_rate
            result['ytd_income'] = biweekly_rate * 26
            result['gmi'] = result['ytd_income'] / 12
        elif income_type == 'monthly':
            monthly_rate = float(data.get('monthlyRate', 0))
            if monthly_rate <= 0:
                print("Invalid monthly rate")
                return render_template('gmi.html', error='Monthly rate must be positive')
            result['rate'] = monthly_rate
            result['ytd_income'] = monthly_rate * 12
            result['gmi'] = monthly_rate
        elif income_type == 'annual':
            annual_rate = float(data.get('annualRate', 0))
            if annual_rate <= 0:
                print("Invalid annual rate")
                return render_template('gmi.html', error='Annual rate must be positive')
            result['rate'] = annual_rate
            result['ytd_income'] = annual_rate
            result['gmi'] = annual_rate / 12
        else:
            print("Invalid income type")
            return render_template('gmi.html', error='Invalid income type')

        print("Rendering gmi.html with result:", result)
        return render_template('gmi.html', result=result)
    
    except (ValueError, TypeError) as e:
        print(f"Error in POST: {e}")
        return render_template('gmi.html', error=f'Invalid data format: {str(e)}')

@app.route('/three-month-income', methods=['GET', 'POST'])
def three_month_income():
    print("Accessing /three-month-income route")
    if request.method == 'GET':
        return render_template('three-month-income.html')
    
    print("Handling POST request")
    data = request.form.to_dict()
    print("Received form data:", data)
    print("Data received:", data)

    # Initialize totals for each month
    month1_income = 0
    month2_income = 0
    month3_income = 0

    # Sum incomes for each month
    for key, value in data.items():
        print(f"{key}: {value}")
        try:
            if value:  # Check if value is not empty
                income_value = float(value)
                if income_value < 0:
                    print("Negative income value")
                    return render_template('gmi.html', error='Income values cannot be negative')
                if key.startswith('month1'):
                    month1_income += income_value
                    print(f"Month 1 Income Total: {month1_income}")
                elif key.startswith('month2'):
                    month2_income += income_value
                    print(f"Month 2 Income Total: {month2_income}")
                elif key.startswith('month3'):
                    month3_income += income_value
                    print(f"Month 3 Income Total: {month3_income}")
        except ValueError:
            print(f"Invalid income value for {key}: {value}")
            return render_template('gmi.html', error=f'Invalid income value: {value}')
        
    total_income = month1_income + month2_income + month3_income
    gmi = total_income / 3 if total_income else 0
    print(f"Total Income: {total_income}, GMI: {gmi}")


    result = {
        'gmi': gmi,
        'message': "This is the customer's Gross Monthly Income calculated based on Bank Deposits"
    }
    print("Rendering gmi.html with result:", result)
    return render_template('gmi-1099.html', result=result)

if __name__ == '__main__':
    port = 5000
    try:
        print(f"Starting server on port {port}...")
        app.run(debug=True, port=port)
    except socket.error as e:
        print(f"Error starting server on port {port}: {e}")
        port = 5001
        print(f"Trying port {port}...")
        try:
            app.run(debug=True, port=port)
        except socket.error as e:
            print(f"Error starting server on port {port}: {e}")
            print("Please free up port 5000 or 5001 or specify a different port.")
            exit(1)