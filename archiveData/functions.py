import urllib.request
import re

regex1 = r"""<th valign="top" width="14%"><strong>Incident:</strong></th>"""
incidentPattern = re.compile(regex1)

def save_page(x):

    url = x

    fName = "savedPage.html"

    response = urllib.request.urlopen(url)

    webContent = response.read().decode('utf-8')

    #print(webContent)

    try:
        f = open(fName, 'x', encoding='utf-8')
        f.write(webContent)
        f.close()
    except FileExistsError:
        print()
        print("File output error: a file named {} already exists. Using existing file.".format(fName))

    return fName

def parse_data(line):
    pass