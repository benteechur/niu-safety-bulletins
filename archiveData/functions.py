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

regex4 = r"""<td valign="top"><strong>Location: </strong></td>"""
locationPattern = re.compile(regex4)

regex5 = r"""(<td valign="top">)(.*)(</td>)"""
locationDataPattern = re.compile(regex5)

# pattern for stripping off one set of tags
regex6 = r"""<.*>(.*)</.*>"""
stripTagPattern1 = re.compile(regex6)

# pattern for stripping off two sets of tags
regex7 = r"""<.*><.*>(.*)</.*></.*>"""
stripTagPattern2 = re.compile(regex7)


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

#def parse_data(line, dateSentinel):
def parse_data(line, sentinel):
    incidentTag = incidentPattern.search(line)
    if incidentTag:
        print("found match: ", incidentTag.group(2))

    dateTag = datePattern.search(line)
    if dateTag:
        #dateSentinel[0] = True
        sentinel["date"] = True
        # return immediately from function so that rest of function isn't executed
        return
    #if dateSentinel[0]:
    if sentinel["date"]:
        dateDataTag = dateDataPattern.search(line)
        if dateDataTag:
            print("found date data: ", dateDataTag.group(2))
            #dateSentinel[0] = False
            sentinel["date"] = False

    locationTag = locationPattern.search(line)
    if locationTag:
        sentinel["location"] = True
        return
    if sentinel["location"]:
        locationDataTag = locationDataPattern.search(line)
        if locationDataTag:
            print("found location data: ", locationDataTag.group(2))
            temp = locationDataTag.group(2)
            if "<" in temp:
                print("extra tags here")
                locationStripTag = stripTagPattern1.search(temp)
                # if a group is empty, it is equal to an empty string
                if locationStripTag.group(1) == "":
                    locationStripTag = stripTagPattern2.search(temp)
                    newTemp = locationStripTag.group(1)
                else:
                    newTemp = locationStripTag.group(1)
                print("strippping tags from location data: ", newTemp)
            sentinel["location"] = False