import re
import pandas as pd

# Function:  function to create new "Crime Type" column and update the df
# Arguments: takes a dataframe
# Returns:   nothing (updates the df in place)

crime_lst = ['robbery', 'battery', 'burglary', 'burglaries', 'theft', 'firearm',
'shots', 'shooting', 'fire', 'arson', 'assault', 'invasion']
crime_re_lst = [re.compile(r'\b' + i + r'\b') for i in crime_lst]

def add_crime_type(df):
    new_value = []
    for j in df.iloc[:,0].str.lower():
        temp_lst = []
        for i in crime_re_lst:
            match = i.search(j)
            if match:
                temp_lst.append(match.group())
        length = len(temp_lst)
        if length == 0:
            temp = ""
        elif length == 1:
            temp = temp_lst[0]
        else:
            temp = temp_lst[0]
            for i in range(1, length):
                temp += ", " + temp_lst[i]
        new_value += [temp]
    df['Crime Type'] = new_value
