from datetime import date
import holidays

# Select country
us_holidays = holidays.US()

# If it is a holidays then it returns True else False
print('01-01-2018' in us_holidays)
print('02-01-2018' in us_holidays)
print('02-01-2017' in us_holidays)

# What holidays is it?
print(us_holidays.get('01-01-2018'))
print(us_holidays.get('02-01-2018'))
