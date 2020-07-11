import requests as req
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename='error.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def get_webpage(url):
    resp = req.get(url)
    if(resp.status_code != 200):
        return None
    else:
        return resp.text

def get_webpage_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def get_list(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    companies = []
    urls = []
    cList = []
    for link in soup.find_all('a', attrs = {'class':'100link'}):
        if("http://www.econtentmag.com/Articles/ArticleReader" not in str(link.get('href'))):
            companies.append(link.get_text())
            urls.append(link.get('href'))
    if(len(companies)==len(urls)):
        for l in range(len(companies)):
            cList.append(list([companies[l],urls[l]]))
    return cList

def get_contact_page_link(html):
    soup1 = BeautifulSoup(html, 'html.parser')
    addLinks = []
    comp = []
    for i in soup1.find_all('a', attrs={'class': '100link'}):
        if("http://www.econtentmag.com/Articles/ArticleReader" not in str(i.get('href'))):
            comp.append(i.get('href'))
    for i in range(15,26):
        try:
            res = req.get(str(comp[i]))
            soup = BeautifulSoup(res.text, 'html.parser')
            for j in soup.find_all('a', href=True):
                if ("Contact" in str(j)):
                    if ("http" not in str(j.get('href'))):
                        addLinks.append(str(comp[i]) + str(j.get('href')))
                    else:
                        addLinks.append(str(j.get('href')))
                elif ("About" in str(j)):
                    if ("http" not in str(j.get('href'))):
                        addLinks.append(str(comp[i]) + str(j.get('href')))
                    else:
                        addLinks.append(str(j.get('href')))
        except req.exceptions.HTTPError as e:
            logging.warning(e)
    add_links = list(dict.fromkeys(addLinks))
    return add_links

def get_location(text):
    return


if __name__ == "__main__":
    wbp = get_webpage(
        "http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm")
    # print(wbp)
    # wbpt = get_webpage_text(wbp)
    # print(wbpt)
    # list = get_list(wbp)
    # print(list)
    contacts = get_contact_page_link(wbp)
    print(contacts)
    # loc = get_location(wbpt)
    # print(loc)