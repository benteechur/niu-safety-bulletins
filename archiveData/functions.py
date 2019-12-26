import urllib.request
import re

# groups in regex1 are as follows:
# group 1: the opening tag for all Incident titles
# group 2: .*, i.e., 0 or more characters of anything
# group 3: the closing tag
# NOTE: regex3 is very similar to regex1 except it is looking for the data for the date field 
regex1 = r"""(<th valign="top" width="86%">)(.*)(</th>)"""
incidentPattern = re.compile(regex1)

regex2 = r"""<td valign="top"><strong>Date Occurred:</strong></td>"""
datePattern = re.compile(regex2)

regex3 = r"""(<td valign="top">)(.*)(</td>)"""
dateDataPattern = re.compile(regex3)


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

def parse_data(line, dateSentinel):
    incidentTag = incidentPattern.search(line)
    if incidentTag:
        print("found match: ", incidentTag.group(2))
    dateTag = datePattern.search(line)
    if dateTag:
        dateSentinel[0] = True
        # return immediately from function so that rest of function isn't executed
        return
    if dateSentinel[0]:
        dateDataTag = dateDataPattern.search(line)
        if dateDataTag:
            print("found date data: ", dateDataTag.group(2))
            dateSentinel[0] = False
