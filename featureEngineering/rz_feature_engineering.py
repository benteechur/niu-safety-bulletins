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

# Rearrange the columns order
df = df[['Incident', 'Crime Type', 'Date Occurred', 'Location',
                 'Location_map', 'Details']]

# Export the dfs after data engineering
df.to_csv(path + r'\feature_bulletin.csv', index = False, encoding = 'utf-8-sig')
print('\n"feature_bulletin.csv" exported successfully!\n')
