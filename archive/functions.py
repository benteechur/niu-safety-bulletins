import urllib.request

def save_page(x):

    url = x

    fName = "savedPage.html"

    response = urllib.request.urlopen(url)

    webContent = response.read().decode('utf-8')

    #print(webContent)

    f = open(fName, 'x', encoding='utf-8')
    f.write(webContent)
    f.close()

    return fName
