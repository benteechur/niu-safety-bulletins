import urllib.request

def get_page(x):

    url = x

    response = urllib.request.urlopen(url)

    webContent = response.read().decode('utf-8')

    #print(webContent)

    return webContent
