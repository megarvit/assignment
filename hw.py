import csv
from datetime import datetime, timedelta

# Define the file path
file_path = 'hw.csv'

# Function to check if an employee worked for 7 consecutive days
def has_worked_for_7_consecutive_days(dates):
    dates = sorted(dates)
    for i in range(len(dates) - 6):
        if all((dates[i + j] - dates[i + j - 1]).days == 1 for j in range(1, 7)):
            return True
    return False

# Function to check if an employee has less than 10 hours between shifts
def has_less_than_10_hours_between_shifts(dates):
    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).seconds < 36000 and (dates[i] - dates[i - 1]).seconds > 3600:
            return True
    return False

# Function to check if an employee has worked for more than 14 hours in a single shift
def has_worked_more_than_14_hours_in_a_single_shift(hours_worked):
    return max(hours_worked) > 14

# Open and read the CSV file
with open(file_path, 'r') as file:
    csv_reader = csv.DictReader(file)
    
    # Create dictionaries to store data for each employee
    employees = {}
    
    for row in csv_reader:
        name = row['Employee Name']
        position = row['Position ID']
        time_value = row['Time']
        
        # Check if the 'Time' value is empty or missing
        if not time_value:
            continue  # Skip this row and continue with the next
        
        # Adjust the datetime format for your date and time format
        date = datetime.strptime(time_value, '%m/%d/%Y %I:%M %p')
        
        # Parse 'Timecard Hours (as Time)' column with format 'HH:MM'
        timecard_hours = row['Timecard Hours (as Time)'].split(':')
        hours_worked = float(timecard_hours[0]) + float(timecard_hours[1]) / 60.0
        
        # Add the data to the employee's record
        if name in employees:
            employees[name]['dates'].append(date)
            employees[name]['hours_worked'].append(hours_worked)
        else:
            employees[name] = {'position': position, 'dates': [date], 'hours_worked': [hours_worked]}

# Iterate through the employee records and apply the criteria
for name, data in employees.items():
    if has_worked_for_7_consecutive_days(data['dates']):
        print(f"{name} (Position ID: {data['position']}) worked for 7 consecutive days.")
    if has_less_than_10_hours_between_shifts(data['dates']):
        print(f"{name} (Position ID: {data['position']}) has less than 10 hours between shifts.")
    if has_worked_more_than_14_hours_in_a_single_shift(data['hours_worked']):
        print(f"{name} (Position ID: {data['position']}) worked for more than 14 hours in a single shift.")
