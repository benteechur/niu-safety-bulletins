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
#df['Year'] = df['Date Occurred'].dt.year
#df['Month'] = df['Date Occurred'].dt.month_name()
#print('\n Month name after extraction:\n', df['Month'].head())
#df['Day'] = df['Date Occurred'].dt.day
# The next line of code only returns the number of week days.
##df['Dayofweek'] = df['Date Occurred'].dt.dayofweek
df['Dayofweek'] = df['Date Occurred'].dt.weekday_name #--> don't need it since Tableau will automatically generate

# Add 'Time' column
extract_time(df, 'Details')
# Add 'Time_24' column
add_time_24(df)
# Convert values in 'Time_24' column into datetime data type
df['Time_24'] = pd.to_datetime(df['Time_24']).dt.time


# Rearrange the columns order
##df = df[['Incident', 'Crime Type', 'Date Occurred', 'Year', 'Month', 'Day',
##         'Dayofweek', 'Time_24', 'Location', 'Location_map', 'Details']]


'''
# Rearrange code for creating time related columns to work better in Tableau
# --> This appear to not work for the records that don't have a specific time.
# Add 'Time_24' column
extract_time(df, 'Details')
add_time_24(df)
# Combine date and time to create new datetime type column 'DateTime'
##df['DateTime'] = [pd.to_datetime(df['Date Occurred'][x]) if pd.isna(df['Time_24'][x])
##                  else pd.to_datetime(df['Date Occurred'][x] + ' ' + df['Time_24'][x])
##                  for x in range(0, df.shape[0])]
df['DateTime'] = pd.to_datetime(df['Date Occurred'] + ' ' + df['Time_24'])

# Convert 'Date Occurred' column to datetime type to create new column 'Dayofweek'
df['Date Occurred'] = pd.to_datetime(df['Date Occurred'])
df['Dayofweek'] = df['Date Occurred'].dt.weekday_name

print('\ndf before adding coordinates:\n', df.head(20))
#print('\nif latitude or longitude in df: ', 'Location_map' in df.columns)
'''
# Add 'Latitude' and 'Longitude' columns
add_latlng(df)

#print('\nto check time for cell 36:', df['Time_24'][36])

# Rearrange columns order
##df = df[['Incident', 'Crime Type', 'DateTime', 'Dayofweek', 'Location',
##         'Latitude', 'Longitude', 'Details']]
df = df[['Incident', 'Crime Type', 'Date Occurred', 'Time_24', 'Dayofweek',
         'Location', 'Location_map', 'Latitude', 'Longitude', 'Details']]

#print('\n The df after adding latlng is: \n', df.head(38))


# Export the dfs after data engineering
df.to_csv(path + r'\feature_bulletin.csv', index = False, encoding = 'utf-8-sig')
print('\n"feature_bulletin.csv" exported successfully!\n')
