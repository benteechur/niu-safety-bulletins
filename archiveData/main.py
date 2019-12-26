from functions import *
import Bulletin as B

url = 'https://www.niu.edu/publicsafety/emergency/safetybulletin/archive.shtml'
# make dateSentinel a list so that the value may be updated (bools are immutable in Python, while lists aren't)
dateSentinel = [False]

# the entire contents of the page at "url" are now saved in a file named fileName
fileName = save_page(url)

#print(fileName)

try:
    file = open(fileName, 'r', encoding='utf-8-sig')
except IOError:
    print()
    print("Cannot open", fileName)
    print()
    exit()

line_count = 0

for line in file:
    line_count += 1
    parse_data(line, dateSentinel)

print(line_count)
