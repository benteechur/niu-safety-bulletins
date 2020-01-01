# Import packages
import pandas as pd
from functions import *

# Set the maximum number of columns and rows
# so that all the df columns and rows can be shown
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_columns', 100)


# Import semi-cleaned csv files
path = r'C:\Users\zhang\Desktop\Test files'     # CHANGE ME
df_new = pd.read_csv(path + r'\clean_new_bulletin.csv')
df_old = pd.read_csv(path + r'\clean_old_bulletin.csv')
print('df_new before cleaning:\n', df_new)
print()
print('The first 15 lins of df_old before cleaning:\n', df_old.head(15))
print()

#df_new['Location'] = df_new['Location'].str.lstrip() #--> eliminate the white
# space at the beginning of cells

# Add "Crime Type" column
add_crime_type(df_new)
add_crime_type(df_old)

print()
print('df_old after adding new column:\n', df_old[['Incident', 'Crime Type']].head(30))
print()
print('df_new after adding new column:\n', df_new[['Incident', 'Crime Type']].head(30))
print()

# Export the dfs after data engineering
path = r'C:\Users\zhang\Desktop\Test files'
df_new.to_csv(path + r'\feature_new_bulletin.csv', index = False)
df_old.to_csv(path + r'\feature_old_bulletin.csv', index = False)
