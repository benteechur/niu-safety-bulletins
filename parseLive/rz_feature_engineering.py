# Import packages
import pandas as pd
import re

# Set the maximum number of columns and rows
# so that all the df columns and rows can be shown
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_columns', 100)


# Import semi-cleaned csv files
path = r'D:\1Study\Git\niu-safety-bulletins\Test files'     # CHANGE ME
df_new = pd.read_csv(path + r'\new_notifications1.csv')
df_old = pd.read_csv(path + r'\old_notifications1.csv')
print('df_new before cleaning:\n', df_new)
print()
print('The first 15 lins of df_old before cleaning:\n', df_old.head(15))
print()


# ************* Create df for showing on map *********************************
#df_new['Location'] = df_new['Location'].str.lstrip() #--> eliminate the white
# space at the beginning of cells


crime_lst = ['robbery', 'burglary', 'burglaries', 'theft', 'firearm', 'shots',
'shooting', 'fire', 'arson', 'assault', 'invasion']


#crime_lst = [re.compile(r'\brobbery\b'), re.compile(r'\bburglary\b'), re.compile(r'\bburglaries\b'), re.compile('theft'), re.compile('firearm'),
#re.compile('shots'), re.compile('shooting'), re.compile(r'\bfire\b'), re.compile('arson'), re.compile('assault'), re.compile('invasion')]
#print(crime_lst)

test_lst = [re.compile(r'\b' + i + r'\b') for i in crime_lst]
print(test_lst)
#subcrime_lst = ['strong armed', '']

#print('The "Incident" of the first record is:', df_new.iloc[0,0] )
new_value = []
for j in df_old.iloc[:,0].str.lower():
    temp_lst = []
    ##for i in crime_lst:
    for i in test_lst:
        match = i.search(j)
        if match:
        ##if i in j:
            #df_new['Crime Type'][j] = i
            ##temp_lst.append(i)
            temp_lst.append(match.group())
        #else:
            #temp_lst = 'NaN'
    new_value.append(temp_lst)
#new_value = [i for i in crime_lst if i in (df_new.iloc[0][j] for j in range(0, df_new.shape[0]))]
#new_value = [[i]]
print(new_value)
print()
df_old['Crime Type'] = new_value

print()
print('df_new after adding new column:\n', df_old[['Incident', 'Crime Type']].head(30))

# Create new columns 'City' and 'States'
#city_lst = []
#print('df_new after cleaning:\n', df_new)
