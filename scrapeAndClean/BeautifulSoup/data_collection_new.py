# Import necessary packages

import requests, time, re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Set url and access the site with requests lib

url_new = 'https://www.niu.edu/publicsafety/emergency/safetybulletin/index.shtml'
url_old = 'https://www.niu.edu/publicsafety/emergency/safetybulletin/archive.shtml'
#response = requests.get(url_new)

response_new = urlopen(url_new)
response_old = urlopen(url_old)

# Parse the html with BeautifulSoup

#soup = BeautifulSoup(response.text, 'html.parser')
soup_new = BeautifulSoup(response_new, 'lxml')
soup_old = BeautifulSoup(response_old, 'lxml')

# Get the title
title_new = soup_new.title
title_old = soup_old.title
print(title_new)
print(title_old)

# Print out the text as well
#text2 = soup2.get_text()
#text = soup.get_text()
#print(text)

# Use the method .findAll to locate <tr> tags
# < a > for hyperlinks, < table > for tables, < tr > for table rows,
# < th > for table headers, and < td > for table cells

rows_new = soup_new.find_all('tr')
print('The first two rows from new safety notifications:')
print(rows_new[:2])
#print()
#print()
#print(soup_new.find_all('tr'))
#print(rows_new[0])

print('\n------------------------------------------------------------------\n')

rows_old = soup_old.find_all('tr')
print('The first two rows from archived safety notifications:')
print(rows_old[:2])
print()
print()

# Have a look at the headers from new safety notifications
headers = soup_new.find_all('th')
print(headers[:])

# Calulate elapsed time and cpu time (start)
start_elapsed = time.perf_counter()
start_cpu = time.process_time()

# Put the data that was scraped from web into a dataframe
safety_lst = []
row_lst = []

for row in rows_new:
    row_header = row.find_all('th')
    str_header = str(row_header)
    clean_header = BeautifulSoup(str_header, 'lxml').get_text()
    splitted_header = re.split('[-,]', clean_header)
    #print('The splitted header is: ', splitted_header)
    #print('The cleaned row th is: ', clean_header)
    #print('The length of "*row_header": ', len(*row_header))
    #print()

    row_content = row.find_all('td')
    str_content = str(row_content)
    clean_content = BeautifulSoup(str_content, 'lxml').get_text()
    splitted_content = re.split(r': ,|:,', clean_content)
    #print('The cleaned row td is: ', clean_content)
    #print('The length of the first row td is: ', len(clean_content))
    #print('The fist element in clean_content:', clean_content[0])
    #print('The data type of row_content: ', type(row_content))
    #print('The data type of str_content: ', type(str_content))
    #print()


    if len(clean_header) > 2:
        #safety_lst.append(row_lst)
        safety_lst += [row_lst]
        row_lst = []
        #row_lst.append(clean_header)
        row_lst += splitted_header
    if len(clean_content) > 2:
        #row_lst.append(clean_content)
        row_lst += splitted_content
    #break
        #print("row_lst inside of the loop is: ", row_lst)
#safety_lst.append(row_lst)  # To append the last element
safety_lst += [row_lst]
    #break

# Calulate time (end)
end_elapsed = time.perf_counter()
end_cpu = time.process_time()

print()
#print('The list that contains every notification is: ', safety_lst)
#print('The length of safety_lst is: ', len(safety_lst))
#print('The last element in the safety_lst: ', safety_lst[-1])
#print()
#print()
print('Elapsed time is: ', end_elapsed - start_elapsed)
print('CPU time is:     ', end_cpu - start_cpu)
print()


#****************** Convert the safety_lst into a dataframe ******************
# Set the maximum number of columns so that all the df columns can be shown
pd.set_option('display.max_columns', 100)

##df_header = ['Incident', 'Date Occurred', 'Location', 'Details',
##'tips', 'about']
##df = pd.DataFrame(safety_lst, columns = df_header)
df = pd.DataFrame(safety_lst)
#print(df)

# Clean up the DataFrame
# Dropped the "Safety Tips and Resources" and "About Safety bulletins" columns
##df.drop(['tips', 'about'], axis = 1, inplace = True)
##df.drop([0], axis = 0, inplace = True)

# Split columns at comma and dash positions
##df1 = df

# Drop the last two columns which are "tips and recourse" and "About..."
df.drop([0, 3, 5, 7, 9, 11, 12], axis = 1, inplace = True)
df.drop([0], axis = 0, inplace = True)

# Put header into df:
df_header = ['Notification Type', 'Crime Type', 'On/Off Campus',
'Date Occurred', 'Location', 'Details']
df.columns = df_header

# Delete the "]" in 'On/Off Campus', 'Date Occurred', and 'Location' columns
df['On/Off Campus'] = df['On/Off Campus'].str.rstrip(' ]')
df['Date Occurred'] = df['Date Occurred'].str.rstrip(' ]')
df['Location'] = df['Location'].str.rstrip(' ]')
print(df)
