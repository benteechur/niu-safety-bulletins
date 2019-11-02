from functions import *

url = 'https://www.niu.edu/publicsafety/emergency/safetybulletin/archive.shtml'

# the entire contents of the page at "url" are now contained in the string "webContent"
webContent = get_page(url)

print(webContent)

