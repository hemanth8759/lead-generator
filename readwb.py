import requests as req

def get_webpage(url):
    resp = req.get(url)
    if(resp.status_code != 200):
        return None
    else:
        get_webpage_text(resp.text)
        return resp.text

def get_webpage_text(html):
    return str(html)

get_webpage("http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm")