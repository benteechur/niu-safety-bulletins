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

regex8 = r"""<td valign="top"><strong>Details: </strong></td>"""
detailsPattern = re.compile(regex8)

regex9 = r"""<td valign="top">"""
detailsDataOpenPattern = re.compile(regex9)

regex10 = r"""</td>"""
detailsDataClosePattern = re.compile(regex10)


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

def parse_data(line, sentinel, detailsCat):
    incidentTag = incidentPattern.search(line)
    if incidentTag:
        # print() to separate output by blank line
        print()
        print("found match: ", incidentTag.group(2))

    dateTag = datePattern.search(line)
    if dateTag:
        sentinel["date"] = True
        # return immediately from function so that rest of function isn't executed
        return
    if sentinel["date"]:
        dateDataTag = dateDataPattern.search(line)
        if dateDataTag:
            print("found date data: ", dateDataTag.group(2))
            sentinel["date"] = False

    locationTag = locationPattern.search(line)
    if locationTag:
        sentinel["location"] = True
        return
    if sentinel["location"]:
        locationDataTag = locationDataPattern.search(line)
        if locationDataTag:
            print("found location data: ", locationDataTag.group(2))
            
            # this section for cleaning data - consider placing this in another function
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

    detailsTag = detailsPattern.search(line)
    if detailsTag:
        sentinel["details"] = True
        return
    if sentinel["details"]:
        detailsOpenTag = detailsDataOpenPattern.search(line)
        detailsCloseTag = detailsDataClosePattern.search(line)
        
        if detailsOpenTag:
            sentinel["detailsData"] = True
        if sentinel["detailsData"] and len(line) > 1:
            temp = line.lstrip()
            temp = temp.rstrip()
            # 점 marks the end of a line
            detailsCat[0] += temp + "점"

        if detailsCloseTag:
            temp = detailsCat[0]
            count = temp.count("<")
            for i in range(count):
                begin = temp.find("<")
                end = temp.find (">")
                temp = temp[:begin] + temp[end+1:]

            print("contents of detailsCat: ", detailsCat[0])
            print("contents of temp: ", temp)
            detailsCat[0] = ""
            sentinel["detailsData"] = False
            sentinel["details"] = False

    """
    # original, more difficult way of removing tags
    detailsTag = detailsPattern.search(line)
    if detailsTag:
        sentinel["details"] = True
        return
    if sentinel["details"]:
        detailsOpenTag = detailsDataOpenPattern.search(line)
        detailsCloseTag = detailsDataClosePattern.search(line)
        if detailsOpenTag:
            sentinel["detailsData"] = True
        if sentinel["detailsData"]:
            #print("details sentinel working")
            detailsStripTag = stripTagPattern1.search(line)
            detailsStripTag2 = stripTagPattern2.search(line)
            # python has lazy evaluation so .group(1) can be written as a second condition here
            # despite the fact that many times detailsStripTag will evaluate to None (.group(1)
            # should not be called on None as this will result in an error)
            if detailsStripTag and detailsStripTag.group(1) != "":
                detailsCat[0] += detailsStripTag.group(1)
            if detailsStripTag2 and detailsStripTag2.group(1) != "":
                detailsCat[0] += detailsStripTag2.group(1)
        if detailsCloseTag:
            temp = line[:detailsCloseTag.start()]
            detailsStripTag = stripTagPattern1.search(temp)
            if detailsStripTag:
                #print("contents of temp's group 1: ", detailsStripTag.group(1))
                detailsCat[0] += detailsStripTag.group(1)
            print("contents of detailsCat: ", detailsCat[0])
            detailsCat[0] = ""
            sentinel["detailsData"] = False
            sentinel["details"] = False
    """