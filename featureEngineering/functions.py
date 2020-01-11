import re
import pandas as pd
import numpy as np

# Function:  function to create new "Crime Type" column and update the df
# Arguments: takes a dataframe
# Returns:   nothing (updates the df in place)

crime_lst = ['robbery', 'battery', 'burglary', 'burglaries', 'theft[s]?', 'firearm',
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
            temp = pd.NaT
        elif length == 1:
            temp = temp_lst[0]
        else:
            temp = temp_lst[0]
            for i in range(1, length):
                temp += ', ' + temp_lst[i]
        new_value += [temp]
    df['Crime Type'] = new_value


# Function:  to remove 'DeKalb' from 'Location' column
# Arguments: the string that needs to be removed
# Returns:   another string that gets 'DeKalb' removed

# ',? ?' checks that infront of 'dekalb', there might be a comma or a space or
# both or without either of them
dekalb_pattern = re.compile(r',? ?dekalb\b')
def rm_dekalb(x):
    match = dekalb_pattern.search(x.lower())
    if match:
        str = x[:match.start()] + x[match.end():]
        return str
    else:
        return x

# Function:  function to update the df by adding a new column 'Location_map'
#            which will be used to pin the addresses on Google map.
# Arguments: the df that needs to be updated
# Returns:   nothing (update the original df)

def add_loc_map(df):
    # If record doesn't have a value for 'Crime Type', then don't add address
    # to 'Location_map' column. For the other records, delete the existing 'DeKalb'
    # from the 'Location' column by using rm_dekalb function and then add
    # ', DeKalb, IL 60115' to the Location value to generate Location_map value
    df['Location_map'] = [pd.NaT if pd.isna(df['Crime Type'][x])
                          else rm_dekalb(df['Location'][x]) + ', DeKalb, IL 60115'
                          for x in range(0, df.shape[0])]
