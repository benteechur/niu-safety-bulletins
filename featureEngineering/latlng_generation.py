import pandas as pd

import os, re

# Set the path for exporting files
username = os.environ['username']
path = r'C:\Users' + '\\' + username + r'\Desktop\Test'

# Import semi-cleaned csv files
df = pd.read_csv(path + r'\clean_bulletin.csv')

# Add 'Location_map' column
add_crime_type(df)
add_loc_map(df)

print('\nBefore geocoding\n', df)
# Add coordinates for addresses

# Export the dfs after data engineering
df.to_csv(path + r'\feature_bulletin_coordinates.csv', index = False, encoding = 'utf-8-sig')
print('\n"feature_bulletin_coordinates_.csv" exported successfully!\n')
