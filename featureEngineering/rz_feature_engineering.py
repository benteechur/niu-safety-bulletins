# Import packages
import pandas as pd
from functions import *
import os, re

# Set the path for exporting files
username = os.environ['username']
path = r'C:\Users' + '\\' + username + r'\Desktop\Test'

# Set the maximum number of columns and rows
# so that all the df columns and rows can be shown
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_columns', 100)

# Import semi-cleaned csv files
df = pd.read_csv(path + r'\clean_bulletin.csv')

# Add 'Crime Type' column
add_crime_type(df)

# Add 'Location_map' column
add_loc_map(df)

# Add 'Year', 'Month', and 'Day' columns based on 'Date Occurred'
print('\nDate Occurred column before conversion:\n', df['Date Occurred'])
# Convert 'Date Occurred' column to datetime date type
df['Date Occurred'] = pd.to_datetime(df['Date Occurred'])
##print('\nDate Occurred column after conversion:\n', df['Date Occurred'])
print('\nData type after coversion: \n', df.dtypes)
# Exact month from 'Date Occurred' column
# Method 1 (without converting to datetime data type):
# https://www.interviewqs.com/ddi_code_snippets/extract_month_year_pandas
#df['Month Occurred'] = pd.DatetimeIndex(df['Date Occurred']).month
# Method 2 (has to convert to datetime data type):
df['Year'] = df['Date Occurred'].dt.year
df['Month'] = df['Date Occurred'].dt.month
df['Day'] = df['Date Occurred'].dt.day

# Add 'Time' column
extract_time(df, 'Details')
print('\nafter extraction of time:\n', df['Time'])
print('\nCell 49 after extraction of time is:\n', df['Time'][48])

# Add 'Time_24' column
add_time_24(df)
print('\n"Time_24" column: \n', df['Time_24'].head(30))
print('\ncell 47 for "Time_24" column is:\n', df['Time_24'][47])
# Convert values in 'Time_24' column into datetime data type
df['Time_24'] = pd.to_datetime(df['Time_24'], format = '%H:%M').dt.time
print('\n"Time_24" after conversion is:\n', df['Time_24'].head(35))
print('\ncell 48 of "Time_24" after conversion is: \n', df['Time_24'][48])

# Rearrange the columns order
df = df[['Incident', 'Crime Type', 'Date Occurred', 'Year', 'Month', 'Day',
         'Location', 'Location_map', 'Time', 'Time_24', 'Details']]

# Export the dfs after data engineering
df.to_csv(path + r'\feature_bulletin.csv', index = False, encoding = 'utf-8-sig')
print('\n"feature_bulletin.csv" exported successfully!\n')
