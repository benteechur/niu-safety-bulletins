import urllib.request
import re

# groups in regex1 are as follows:
# group 1: the opening tag for all Incident titles
# group 2: .*, i.e., 0 or more characters of anything
# group 3: the closing tag
regex1 = r"""(<th valign="top" width="86%">)(.*)(</th>)"""

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
    incidentTag = incidentPattern.search(line)
    if incidentTag:
        print("found match: ", incidentTag.group(2))