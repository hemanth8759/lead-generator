import requests as req
from bs4 import BeautifulSoup

def get_webpage(url):
    resp = req.get(url)
    if(resp.status_code != 200):
        return None
    else:
        get_webpage_text(resp.text)
        get_list(resp.text)
        get_contact_page_link(resp.text)
        return resp.text

def get_webpage_text(html):
    return str(html)

def get_list(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    companies = []
    for link in soup.find_all('a', attrs = {'class':'100link'}):
        if("http://www.econtentmag.com/Articles/ArticleReader" not in str(link.get('href'))):
            companies.append(link.get_text()+" = "+link.get('href'))
    return companies

def get_contact_page_link(html):
    soup1 = BeautifulSoup(html, 'html.parser')
    addLinks = []
    for i in soup1.find_all('a', attrs={'class': '100link'}):
        if("http://www.econtentmag.com/Articles/ArticleReader" not in str(i.get('href'))):
            res = req.get(str(i.get('href')))
            soup = BeautifulSoup(res.text, 'html.parser')
            for j in soup.find_all('a', href=True):
                if ("Contact" in str(j)):
                    if ("http:" not in str(j.get('href'))):
                        addLinks.append(str(i) + str(j.get('href')))
                    else:
                        addLinks.append(str(j.get('href')))
                elif ("About" in str(j)):
                    if ("http:" not in str(j.get('href'))):
                        addLinks.append(str(i) + str(j.get('href')))
                    else:
                        addLinks.append(str(j.get('href')))
        addLinks = list(dict.fromkeys(addLinks))
        return addLinks





get_webpage("http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm")