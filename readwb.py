import requests as req

def get_webpage(url):
    resp = req.get(url)
    if(resp.status_code != 200):
        return None
    else:
        get_webpage_text(resp.text)
        get_list(resp.text)
        return resp.text

def get_webpage_text(html):
    return str(html)

def get_list(page_html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_html, 'html.parser')
    companies = []
    for link in soup.find_all('a', attrs = {'class':'100link'}):
        companies.append(link.get_text()+" = "+link.get('href'))
    return companies


get_webpage("http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm")