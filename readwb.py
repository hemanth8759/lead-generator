import requests as req

def get_webpage(url):
    resp = req.get(url)

    return resp.text


get_webpage("http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm")