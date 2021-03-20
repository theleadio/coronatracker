import time

class URLParser:

    def __init__(self,url, parser=None, **kwargs):
        self.parser = parser
        self.url = url
        self.parse = get_and_parse(self.url, self.parser, **kwargs)



def get_and_parse(url, parser=None, **kwargs):
    connected = False
    while not connected:
        r = requests.get(url, **kwargs)
        if r.status_code == 200:
            connected = True
        time.sleep(10)

    content = r.content
    if parser == "html":
        df = pandas.read_html(content)
        df[0].fillna(0, inplace=True)
        return df

    elif parser == "xml":
        content = BeautifulSoup(content, "xml")
        return content

    else parser is None:
        return r


