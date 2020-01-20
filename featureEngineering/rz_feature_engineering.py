# Import packages
import pandas as pd
from functions import *
import os, re
import googlemaps

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

# Add 'Year', 'Month', 'Day', and 'Dayofweek' columns based on 'Date Occurred'
# Convert 'Date Occurred' column to datetime date type
df['Date Occurred'] = pd.to_datetime(df['Date Occurred'])
# Exact month from 'Date Occurred' column
# Method 1 (without converting to datetime data type):
# https://www.interviewqs.com/ddi_code_snippets/extract_month_year_pandas
#df['Month Occurred'] = pd.DatetimeIndex(df['Date Occurred']).month
# Method 2 (has to convert to datetime data type):
# The next line of code only returns the number of week days.
##df['Dayofweek'] = df['Date Occurred'].dt.dayofweek
#--> don't really need it if using Tableau, but I'll keep it here
df['Dayofweek'] = df['Date Occurred'].dt.weekday_name

# Add 'Time' column
extract_time(df, 'Details')
# Add 'Time_24' column
add_time_24(df)

# Rearrange columns order for exporting the df_mymap.csv file
df_mymap = df[['Incident', 'Crime Type', 'Date Occurred', 'Time_24', 'Dayofweek',
               'Location_map', 'Details']]

# Convert values in 'Time_24' column into datetime data type
# (didn't convert it above because don't want to show two seconds digits on
# Google map)
df['Time_24'] = pd.to_datetime(df['Time_24']).dt.time

# Add 'Latitude' and 'Longitude' columns
add_latlng(df)

# Rearrange columns order for exporting df_tableau.csv file
df_tableau = df[['Incident', 'Crime Type', 'Date Occurred', 'Time_24', 'Dayofweek',
         'Location', 'Location_map', 'Latitude', 'Longitude', 'Details']]

# Export the dfs after data engineering
df_tableau.to_csv(path + r'\feature_bulletin_tableau.csv', index = False, encoding = 'utf-8-sig')
df_mymap.to_csv(path + r'\feature_bulletin_mymap.csv', index = False, encoding = 'utf-8-sig')
print('\nBoth "feature_bulletin_tableau.csv" and "feature_bulletin_mymap.csv" exported successfully!\n')
