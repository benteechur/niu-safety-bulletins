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
        splitted_header = re.split(r'Incident:', clean_header)

        row_content = row.find_all('td')
        str_content = str(row_content)
        clean_content = BeautifulSoup(str_content, 'lxml').get_text()
        splitted_content = re.split(r': ,|:,', clean_content)

        if len(clean_header) > 2:
            safety_lst += [row_lst]
            row_lst = []
            row_lst += splitted_header
            #row_lst += [clean_header]
        if len(clean_content) > 2:
            row_lst += splitted_content
    safety_lst += [row_lst]
    return safety_lst


# Function:  Clean the df after it's converted from a list to a df
#            by dropping useless columns and rows, getting rid of "]", splitting
#            the first column (header in the table), and resetting index.
# Arguments: A df
# Returns:   Another df that is cleaned

def clean_df(df):
    # Drop useless columns and rows
    #df.drop([0, 2, 4, 6, 8, 9, 10, 11, 12], axis = 1, inplace = True)
    df.drop(df.columns[8:], axis = 1, inplace = True)
    df.drop([0, 2, 4, 6], axis = 1, inplace = True)
    df.drop([0], axis = 0, inplace = True)
    #print('after dropping: \n', df)
    # Get rid of "]"
    df[1] = df[1].str.rstrip(' ]')
    df[1] = df[1].str.lstrip(', ')
    df[3] = df[3].str.rstrip(' ]')
    df[5] = df[5].str.rstrip(' ]')
    df[7] = df[7].str.rstrip(' ]')
    # Split the first column
    ##df[1] = df[1].str.split(' - ')
    ##df.reset_index(inplace = True)
    ##df_title_column = pd.DataFrame(df[1].values.tolist())
    # Concated the splitted first columns with the original df and then dropped
    # the unsplitted first column
    ##df_clean = pd.concat([df_title_column, df], axis = 1, ignore_index = True)
    ##df_clean.reset_index(inplace = True)
    ##df_clean.drop(['index', 2, 4, 5], axis = 1, inplace = True)
    # Convert integer labels into actual names
    ##df_header = ['Notification Type', 'Crime Type', 'On/Off Campus',
    ##'Date Occurred', 'Location', 'Details']
    ##df_clean.columns = df_header

    ## TEST
    #df.reset_index(inplace = True)
    #print('the index column is\n', df['index'])

    #df.reset_index(drop = True, inplace = True)
    #df.drop(['index'], axis = 1, inplace = True)
    ##return df_clean

    df_header = ['Incident', 'Date Occurred', 'Location', 'Details']
    df.columns = df_header
    return df

# Function:  the function to test nan values in a column
# Arguments: takes a df and the number of the column that want to be tested
# Return:    the count number of nan values in that column

def count_nan(df, col):
    num = df[col].isna().sum()
    return num
