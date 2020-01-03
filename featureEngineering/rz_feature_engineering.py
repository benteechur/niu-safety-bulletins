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
df_new = pd.read_csv(path + r'\clean_new_bulletin.csv')
df_old = pd.read_csv(path + r'\clean_old_bulletin.csv')
print('df_new before cleaning:\n', df_new)
print()
print('The first 15 lins of df_old before cleaning:\n', df_old.head(15))
print()

#df_new['Location'] = df_new['Location'].str.lstrip() #--> eliminate the white
# space at the beginning of cells

# Add 'Crime Type' column
add_crime_type(df_new)
add_crime_type(df_old)

# Add 'Location_map' column
add_loc_map(df_new)
add_loc_map(df_old)

# Rearrange the columns order
df_old = df_old[['Incident', 'Crime Type', 'Date Occurred', 'Location',
                 'Location_map', 'Details']]

print('df_new after adding city is:\n', df_new)
print()
print('The updated location of record 35 is: ', df_old['Location_map'][35])
print('The updated location of the last record is: \n', df_old['Location_map'][82])
print('The updated locations for top 10 records: ', df_old[['Location_map']].head(10))

# Export the dfs after data engineering
df_new.to_csv(path + r'\feature_new_bulletin.csv', index = False, encoding = 'utf-8-sig')
df_old.to_csv(path + r'\feature_old_bulletin.csv', index = False, encoding = 'utf-8-sig')
