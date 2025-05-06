# Income Calculator

The Income Calculator is a Flask-based web application that calculates Gross Monthly Income (GMI) for W2 and 1099 income types. It supports Year-to-Date (YTD) income, detailed income breakdowns (e.g., hourly, weekly, monthly rates), and a three-month average for 1099 income, making it ideal for financial affidavits or eligibility assessments (e.g., meeting 125% Federal Poverty Guideline thresholds).

# Table of Contents
- Features
- Installation
- Usage
- API Endpoints
- Troubleshooting
- Contributing
- License

## Features
- W2 Income Calculation: Supports YTD income or detailed breakdowns (hourly, weekly, biweekly, monthly, annual).
- 1099 Income Calculation: Supports YTD income, detailed breakdowns, or a three-month average with multiple income entries per month.
- Dynamic Forms: Add multiple income entries per month in the three-month average flow.
- Error Handling: Input validation with clear error messages.
- Extensible: Easily add new income types or integrate external APIs for salary comparisons.

## Installation
- Prerequisites
- Python 3.8+: Download Python
- pip: Python package manager (included with Python)
- Git: To clone the repository (optional)
- Virtual Environment: Recommended to isolate dependencies

### Steps
1. Clone the Repository:
  git clone https://github.com/your-username/income-calculator.git
  cd income-calculator

    Note: Replace your-username with your GitHub username. If you haven’t hosted this on GitHub yet, manually create the project directory and copy the files into it.

2. Set Up a Virtual Environment:
  python -m venv .venv
  - Activate the virtual environment:On Windows:.venv\Scripts\activate
  - Activate the virtual environment: On macOS/Linux: source .venv/bin/activate
    
3. Install Dependencies:
  pip install flask
  Note: The app requires an income.py module with gmi_w2, gmi_1099, and calculate_time functions. Ensure this file is implemented (see Troubleshooting for details).

4. Verify Directory Structure: Ensure the following structure:

<pre> 
  income-calculator/
  ├── server.py
  ├── income.py
  ├── templates/
  │   ├── index.html
  │   ├── w2-income.html
  │   ├── 1099-income.html
  │   ├── year-to-date.html
  │   ├── w2-details.html
  │   ├── 1099-details.html
  │   ├── three-month-income.html
  │   └── gmi.html
  ├── README.md
  └── LICENSE </pre> 
  

5. Start the Server:
    python server.py
  The server runs on http://127.0.0.1:5000 (or 5001 if port 5000 is in use). You’ll see:

  Starting server on port 5000...
   * Serving Flask app 'server' (lazy loading)
   * Environment: development
   * Debug mode: on
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

## Usage
### Accessing the Application

Open a browser and navigate to http://127.0.0.1:5000/. The home page (index.html) links to W2 and 1099 income flows. Alternatively, access directly:
- W2 Income: http://127.0.0.1:5000/w2-income
- 1099 Income: http://127.0.0.1:5000/1099-income

### W2 Income Flow
1. Start at W2 Income Page:
  - Go to http://127.0.0.1:5000/w2-income.
  - Enter a start date (e.g., via URL: ?year=2025&month=5&day=6) and YTD income.
2. Enter YTD Income:
- Choose:
  - Numeric YTD Income (e.g., $50000.00).
  - No YTD Income (proceed to detailed entry).
- Submit
  
3. Detailed Income Entry (if No YTD):
- Redirected to w2-details.html.
- Select income type (hourly, weekly, etc.) and enter rates (e.g., $25.50/hour, 40 hours/week).
- Submit to calculate GMI.

4. View Results:
- Results on gmi.html show:
  - Start Date
  - Income Type
  - Rate
  - Hours per Week (if hourly)
  - YTD Income
  - Gross Monthly Income (GMI)
  - Message

### 1099 Income Flow
1. Start at 1099 Income Page:
- Go to http://127.0.0.1:5000/1099-income?year=2025&month=5&day=6.
2. Choose YTD Income Option:
- Select:
  - No YTD Income (detailed entry).
  - Numeric YTD Income (e.g., $60000.00).
  - Three-Month Average.
- Submit.
3. Three-Month Average (if Selected):
- Redirected to three-month-income.html.
- Enter incomes for April, March, February 2025:
  - Add multiple entries per month (e.g., $5000.50, $3000.75 for April).
  - Use "Add Income" and "Remove" buttons as needed.
- Submit.
4. View Results:
- Results on gmi.html (e.g., GMI of $5767.17 for total $17301.50 over 3 months).

### Example Usage

#### Scenario: Calculate 1099 GMI using a three-month average.
- Steps:
  1. Go to http://127.0.0.1:5000/1099-income?year=2025&month=5&day=6.
  2. Select "Three-Month Average".
  3. Enter:
     - April 2025: $5000.50, $3000.75.
     - March 2025: $4500.25.
     - February 2025: $4800.00.
  4. Submit.
- Result:
    - GMI: $5767.17 ((5000.50 + 3000.750) + 4500.25 + 4800.00) / 3)
    - YTD Income: $17301.50

## API Endpoints
- GET / or /index: Home page (index.html).
- GET /w2-income: W2 income form.
- GET|POST /year-to-date: W2 YTD income processing.
- GET|POST /w2-details: W2 detailed income processing.
- GET|POST /1099-income: 1099 income form and processing.
- GET|POST /1099-details: 1099 detailed income processing.
- POST /three-month-income: 1099 three-month average processing.
    - Form Data: month1Income1, month2Income1, etc.
- GET /gmincome: JSON GMI endpoint (not fully implemented).

## Troubleshooting
- Port Conflict:
  - Error: Error starting server on port 5000.
  - Fix: Check port usage (netstat -aon | findstr :5000 on Windows) and kill the process (taskkill /PID <PID> /F).
- Form Submission Fails:
  - Ensure all fields are filled and values are positive.
  - Check console logs for errors (e.g., Invalid data format).
- Incorrect GMI:
  - Verify income.py functions (gmi_w2, gmi_1099).
  - Check summation in /three-month-income (console logs show running totals).
- Missing income.py:
  - The app requires income.py with gmi_w2, and calculate_time. 

## Contributing
### Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (git checkout -b feature/your-feature).
3. Commit changes (git commit -m "Add your feature").
4. Push to the branch (git push origin feature/your-feature).
5. Open a Pull Request.

## Development Ideas
- Add API integration with BLS OEWS for profession-based salary comparisons.
- Support dynamic month counts in the three-month flow.
- Add user authentication for saving calculations.

## License
This project is open for all. 
