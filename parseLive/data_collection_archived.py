# Import necessary packages
import requests, time, re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Set url and access the site with requests lib
url_old = 'https://www.niu.edu/publicsafety/emergency/safetybulletin/archive.shtml'
response_old = urlopen(url_old)

# Parse the html with BeautifulSoup and find all the <tr> tag
soup_old = BeautifulSoup(response_old, 'lxml')
rows_old = soup_old.find_all('tr')

# Calulate elapsed time and cpu time (start)
start_elapsed = time.perf_counter()
start_cpu = time.process_time()

# Put the data that was scraped from web into a dataframe
safety_lst = []
row_lst = []

for row in rows_old:
    row_header = row.find_all('th')
    str_header = str(row_header)
    clean_header = BeautifulSoup(str_header, 'lxml').get_text()
    splitted_header = re.split('[-,]', clean_header)

    row_content = row.find_all('td')
    str_content = str(row_content)
    clean_content = BeautifulSoup(str_content, 'lxml').get_text()
    splitted_content = re.split(r': ,|:,', clean_content)

    if len(clean_header) > 2:
        safety_lst += [row_lst]
        row_lst = []
        row_lst += splitted_header
    if len(clean_content) > 2:
        row_lst += splitted_content
safety_lst += [row_lst]

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
df = pd.DataFrame(safety_lst)
print(df)

# Clean up the DataFrame: dropped useless columns and rows
df.drop([0, 3, 5, 7, 9, 11, 12], axis = 1, inplace = True)
df.drop([0], axis = 0, inplace = True)
print(df)

# Put header into df:
df_header = ['Notification Type', 'Crime Type', 'On/Off Campus',
'Date Occurred', 'Location', 'Details']
df.columns = df_header

# Delete the "]" in 'On/Off Campus', 'Date Occurred', and 'Location' columns
df['On/Off Campus'] = df['On/Off Campus'].str.rstrip(' ]')
df['Date Occurred'] = df['Date Occurred'].str.rstrip(' ]')
df['Location'] = df['Location'].str.rstrip(' ]')
print(df)
