import requests, time, re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Function:  The function search for useful contents and convert all the records
#            into a nested list.
# Arguments: It takes a list which contains all the content from <tr> tags
# Returns:   A nested list with all the records that are in its own tolist

def process_records(x):
    safety_lst = []
    row_lst = []

    for row in x:
        row_header = row.find_all('th')
        str_header = str(row_header)
        clean_header = BeautifulSoup(str_header, 'lxml').get_text()
        ##splitted_header = clean_header.split(',')
        ##split_header = re.split(r'Incident:', clean_header)
        split_header = re.split(r': ,|:,', clean_header)

        row_content = row.find_all('td')
        str_content = str(row_content)
        clean_content = BeautifulSoup(str_content, 'lxml').get_text()
        split_content = re.split(r': ,|:,', clean_content)

        if len(clean_header) > 2:
            safety_lst += [row_lst]
            row_lst = []
            row_lst += split_header
            #row_lst += [clean_header]
        if len(clean_content) > 2:
            row_lst += split_content
    safety_lst += [row_lst]
    return safety_lst


# Function:  Clean the df after it's converted from a list to a df
#            by dropping useless columns and rows, getting rid of "]", splitting
#            the first column (header in the table), and resetting index.
# Arguments: A df
# Returns:   Another df that is cleaned

def clean_df(df):
    # Drop useless columns and rows
    df.drop(df.columns[8:], axis = 1, inplace = True)
    df.drop([0, 2, 4, 6], axis = 1, inplace = True)
    ##df.drop([0], axis = 0, inplace = True)
    df.dropna(inplace = True)
    #print('after dropping: \n', df) #--> for checking purpose
    # Get rid of useless characters in text
    df[1] = df[1].str.lstrip(', ')
    df[1] = df[1].str.rstrip(' ]')
    df[3] = df[3].str.rstrip(' ]')
    df[5] = df[5].str.rstrip(' ]')
    df[7] = df[7].str.rstrip(' ]')
    # Change the column index
    df_header = ['Incident', 'Date Occurred', 'Location', 'Details']
    df.columns = df_header
    # Remove the redundant part in Details column
    # Commenting out the following two lines of code because it has some
    # mistakes for some records. Will come back later
    #start_pattern = 'If you have any information related to this incident'
    #df['Details'] = [x[:x.find(start_pattern)] for x in df['Details']]
    # Strip white spaces for all the values
    for col in df.columns:
        df[col] = df[col].str.strip()
    return df

# Function:  the function to test nan values in a column
# Arguments: takes a df and the number of the column that want to be tested
# Return:    the count number of nan values in that column

def count_nan(df, col):
    num = df[col].isna().sum()
    return num
