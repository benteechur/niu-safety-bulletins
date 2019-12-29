# Import necessary packages
import requests, time, re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import functions as fns

# Set url and access the site with requests lib
url_old = 'https://www.niu.edu/publicsafety/emergency/safetybulletin/archive.shtml'
response_old = urlopen(url_old)
url_new = 'https://www.niu.edu/publicsafety/emergency/safetybulletin/index.shtml'
response_new = urlopen(url_new)

# Parse the html with BeautifulSoup and find all the <tr> tag
soup_old = BeautifulSoup(response_old, 'lxml')
##, from_encoding = 'utf-8')
rows_old = soup_old.find_all('tr')
soup_new = BeautifulSoup(response_new, 'lxml')
rows_new = soup_new.find_all('tr')

# Calulate elapsed time and cpu time (start)
start_elapsed = time.perf_counter()
start_cpu = time.process_time()

# Put the data that was scraped from web into a dataframe using the function
# "process_records(x)" that stores in the functions.py file
lst_old = fns.process_records(rows_old)
lst_new = fns.process_records(rows_new)

# Calulate time (end)
end_elapsed = time.perf_counter()
end_cpu = time.process_time()

print()
print('Elapsed time is: ', end_elapsed - start_elapsed)
print('CPU time is:     ', end_cpu - start_cpu)
print()

#****************** Convert the safety_lst into a dataframe ******************

# Set the maximum number of columns so that all the df columns can be shown
pd.set_option('display.max_columns', 100)

# Convert the list into df
df_old = pd.DataFrame(lst_old)
df_new = pd.DataFrame(lst_new)

# Clean up the DataFrame using "clean_df(df)" function
df_clean_old = fns.clean_df(df_old)
df_clean_new = fns.clean_df(df_new)

# Print out the cleaned df
print('The cleaned df for archived notifications is:\n', df_clean_old)
print('The cleaned df for new notifications is:\n', df_clean_new)

#********************** Export dataframe to csv files ************************

# Export the two df to xlsx files. (put new version into the same excel file
# but different sheets)
#path_new = r'D:\1Study\Git\niu-safety-bulletins\Test files\new_notifications.xlsx'
#path_old = r'D:\1Study\Git\niu-safety-bulletins\Test files\old_notifications.xlsx'

#writer_new = pd.ExcelWriter(path_new, engine = 'xlsxwriter')
#writer_old = pd.ExcelWriter(path_old, engine = 'xlsxwriter')

#df_clean_new.to_excel(writer_new, sheet_name = 'v1')
#df_clean_old.to_excel(writer_old, sheet_name = 'v1')

#writer_new.save()
#writer_old.save()
#writer_new.close()
#writer_old.close()

# Export the two df to csv files. (will overwrite existing files)
#!!! CHANGE THE PATH BEFORE RUNNING THE CODE
path = r'D:\1Study\Git\niu-safety-bulletins\Test files'
df_clean_new.to_csv(path + r'\new_notifications1.csv', index = False, encoding = 'utf-8-sig')
df_clean_old.to_csv(path + r'\old_notifications1.csv', index = False, encoding = 'utf-8-sig')
