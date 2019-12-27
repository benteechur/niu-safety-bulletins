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


################### Test #############
# export the two df to csv.

df_clean_new.to_csv(r'D:\1Study\Git\niu-safety-bulletins\Test files\new_notifications.csv', index = False)
df_clean_old.to_csv(r'D:\1Study\Git\niu-safety-bulletins\Test files\old_notifications.csv', index = False)
