from functions import save_page

url = 'https://www.niu.edu/publicsafety/emergency/safetybulletin/archive.shtml'

# the entire contents of the page at "url" are now saved in a file named fileName
fileName = save_page(url)

print(fileName)
