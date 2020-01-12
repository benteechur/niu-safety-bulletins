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
        string = x[:match.start()] + x[match.end():]
        return string
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

# Function:  the function convert time into 24-hour time
# Arguments: it takes a string which contains the value of from 'Time' column
# Returns:   the converted string
# Notes:     the purpose to covert time from 12-hour clock to 24-hour clock is
#            for more convenient graphing and clearer data

# Create two Regx patterns:
# - 'time_pattern_digit' matches digital time part. e.g. 11:34 or 7 or 3:45
# - 'time_pattern_am' matches time period
time_pattern_digit = re.compile(r'\d+:*\d*')
time_pattern_am = re.compile(r'a\.*m\.*', re.IGNORECASE)

def convert_hour(x):
    # Assign the pattern matched string to 'match_am' and 'match_digit'
    match_am = time_pattern_am.search(x)
    match_digit = time_pattern_digit.search(x)
    # Assign the value of 'match_digit' to 'digits'
    digits = match_digit.group()
    # First senario: if the value is a morning time (aka the value matches the
    # time_pattern_am) and the first two digit of the time is '12', it will be
    # changed to 0. For example, time 12:30 a.m. in 24-hour clock is displayed
    # as 0:30.
    if match_am and digits[0:2] == '12':
        string = '0' + digits[2:]
    # Second senario: for the rest values that are morning time or the values
    # that are post-midday time but the first two digits of the time is '12',
    # they will be kept as original. For example, a morning time like 7:30 a.m.
    # is also displayed as 7:30 in 24-hour clock; and a noon time like
    # 12:30 p.m. is displayed as 12:30 as well.
    elif match_am or (not match_am and digits[0:2] == '12'):
        string = digits
    # Third senario: all the values that are morning time have been covered in
    # the first two senarios, so the next two senarios are all about afternoon
    # times. If the time was originally represented like 1:30 p.m., 12 will be
    # added to the first digit.
    elif len(digits) == 4:
        string = str(int(digits[0]) + 12) + digits[1:]
    # Fourth senario: the rest of the values which are all supposed to be
    # afternoon times with a format like 10:23 p.m.. For this kind of time,
    # 12 will be added to the first two digits to convert to 24-hour clock.
    else:
        string = str(int(digits[0:2]) + 12) + digits[2:]
    return string


# Function:  function to extract time from 'Details' column
# Arguments: the df and the column that needs to be extracted from
# Returns:   nothing (update the original df)

def extract_time(df, col):
    time_pattern = re.compile(r'''\bat\b\s(.*?) # start with 'at' with or without any other words between 'at' and the time
                                  \d+:*\d*      # time format, such as 7:35
                                  \s            # followed by with or without white spaces
                                  [ap]\.*?m\.*? # a.m. or p.m.''', re.IGNORECASE | re.X)
    df['Time'] = [time_pattern.search(x).group(0) if time_pattern.search(x) else pd.NaT for x in df[col]]

    df['Time_24'] = 0
    for x in range(0, df.shape[0]):
        if pd.isna(df['Time'][x]):
            df['Time_24'][x] = pd.NaT
        else:
            df['Time_24'][x] = convert_hour(df['Time'][x])
