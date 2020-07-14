import requests as req
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename='error.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def get_webpage(url):
    try:
       resp = req.get(url)
       return resp.text
    except req.exceptions.RequestException as e:
        logging.error(e)
        return None

def get_webpage_text(html):
    if(html!= None):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
    else:
        return None

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
    for i in comp:
        try:
            res = req.get(str(i))
            soup = BeautifulSoup(res.text, 'html.parser')
            for j in soup.find_all('a', href=True):
                if ("Contact" in str(j)):
                    if ("http" not in str(j.get('href'))):
                        addLinks.append(str(i) + str(j.get('href')))
                    else:
                        addLinks.append(str(j.get('href')))
                elif ("About" in str(j)):
                    if ("http" not in str(j.get('href'))):
                        addLinks.append(str(i) + str(j.get('href')))
                    else:
                        addLinks.append(str(j.get('href')))
        except req.exceptions.RequestException as e:
            logging.error(e)
        
    add_links = list(dict.fromkeys(addLinks))
    return add_links

def get_location(text):
    if(text != None):
        import re
        addr=[]
        regs = ["(^[0-9]{2,4} .*\n.*[0-9]{2,5}.*\n.*\n)","(^\s[0-9]{2,4} .*\n.*[0-9]{2,5}.*\n.*\n)","(^[0-9]{2,4} .*\n.*\n.*\nUnited States)","(^[0-9]{2,4} .*[0-9]{5})"]
        for rg in regs:
            x = re.findall(rg, str(text),flags = re.M)
            add = "".join(x)
            addr.append(add)
        while("" in addr) : 
            addr.remove("") 
        return addr
    else:
        return None



if __name__ == "__main__":
    wbp = get_webpage(
        "http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm")
    # print(wbp)
    # wbpt = get_webpage_text(wbp)
    # print(wbpt)
    # list = get_list(wbp)
    # print(list)
    contacts = get_contact_page_link(wbp)
    # print(contacts)
    # contactLinks = ['http://acquia.com/about-us', 'http://acquia.com/about-us/contact', 'http://acquiremedia.com/aboutus/', 'http://acquiremedia.com/contactus/', 'http://act-on.com/contact-us/', 'http://act-on.com/why-act-on/our-story/', 'https://act-on.com/contact-us/', 'http://apple.com/contact/', 'http://aptaracorp.com/about-aptara/overview', 'https://www.aquafadas.com/about-us/', 'https://www.aquafadas.com/contact-us/', 'http://aquafadas.com/contact-us/', 'https://global.rakuten.com/corp/about/', 'https://www.ariasystems.com/contact-us/', 'http://ariasystems.com/contact-us/', 'https://www.atex.com/atex/contact-us/', 'https://www.atex.com/atex/about-us/', 'http://atex.com/atex/contact-us/', 'http://attivio.com/solutions/customer-support-search', 'http://attivio.com/company/about-attivio', 'http://attivio.com/contact', 'http://attivio.com/contact?utm_lead_source=OrganicSearch-SEO', 'https://www.atypon.com/about-us/', 'https://www.atypon.com/contact/', 'http://atypon.com/contact', 'http://automattic.com/about/', 'http://automattic.com/contact/', 'http://brightcove.com/en/company/about', 'http://brightcove.com/en/contact-us', 'https://info.brightcove.com/live-streaming-global?cid=70130000000jfgr&pid=7011O0000038d2e', 'https://help.brightcove.com/en/contact/create', 'https://www.ceros.com/about/meet-the-team/', 'https://www.ceros.com/about/contact/', 'http://cision.com/us/contact-us', 'http://cision.com/us/contact-us/', 'http://cision.com/us/about/?nav_location=footer', 'http://cision.com/us/contact-us/?nav_location=footer', 'http://cloudera.com/about.html', 'http://cloudera.comtel:18887891488', 'http://cloudera.com/contact-sales.html', 'http://cloudera.com/contact-us.html', 'https://www.cloudwords.com/about-cloudwords', 'https://www.cloudwords.com/contactus', 'http://cognitivescale.com/contact/', 'http://cognitivescale.com/about/', 'http://contentful.com/contact/sales/', 'http://contentful.com/about-us/', 'http://contentful.com/contact/', 'http://convertmedia.comjavascript:;', 'http://convertmedia.com/contact', 'http://coremedia.com/en/about/contact', 'http://craftersoftware.com#', 'http://craftersoftware.com/about/contact', 'http://crownpeak.com/about/contact-us', 'http://csoftintl.com/contact-us/', 'https://www.csoftintl.com/contact-us/', 'https://www.dnnsoftware.com/about', 'https://www.dnnsoftware.com/about/contact-dnn', 'http://dnnsoftware.com/About/Resources/Whitepapers', 'http://dnnsoftware.com/about', 'http://dnnsoftware.com/about/contact-dnn', 'http://ebsco.com/contact', 'http://ebsco.com/about', 'https://www.elsevier.com/en-in/about', 'http://elsevier.com#footer-661370', 'https://service.elsevier.com/app/overview/elsevier', 'http://episerver.com/company', 'http://episerver.com/contact-us', 'http://frame.iomailto:support@frame.io',
    # 'http://google.com/intl/en/about.html', 'http://onehippo.com#', 'http://onehippo.com/en/about/our-story', 'http://onehippo.com/en/about/contact-us', 'http://onehippo.com', 'https://hootsuite.com/about/contact-us', 'https://hootsuite.com/about', 'http://hubspot.com//offers.hubspot.com/contact-sales', 'http://hubspot.com//www.hubspot.com/our-story', 'http://hubspot.com//www.hubspot.com/company/contact', 'https://help.hubspot.com/', 'https://www.impelsys.com/about-us/', 'https://www.impelsys.com/contact-us/', 'http://kentico.com/we-are-kentico', 'http://kentico.com/contact', 'https://help.salesforce.com/home', 'http://krux.com/company/contact-us/', 'https://www.salesforce.com/company/contact-us/?d=cta-header-9', 'http://krux.com/company/contact-us/?d=cta-header-9', 'https://www.salesforce.com/form/contact/marketingcloud_contactme.jsp?d=70130000000lzZ9', 'http://lingotek.com/company', 'http://lingotek.com/contact', 'https://www.olark.com/site/5763-147-10-7373/contact', 'https://about.linkedin.com/?trk=homepage-basic_directory_aboutUrl', 'https://press.linkedin.com/about-linkedin?trk=homepage-basic_footer-about', 'http://lionbridge.com/who-we-are/#about-us', 'http://lionbridge.com/get-in-touch/', 'https://www.madcapsoftware.com/contact-us/', 'https://www.madcapsoftware.com/support/contact-options.aspx', 'https://www.madcapsoftware.com/customers/customer-success/', 'https://www.madcapsoftware.com/current-promotions/', 'http://madcapsoftware.com/products/', 'http://madcapsoftware.com/solutions/', 'https://www.madcapsoftware.com/company/about-us/', 'http://magnolia-cms.com/about.html', 'http://magnolia-cms.com#', 'http://magnolia-cms.com/contact.html', 'https://help.netflix.com/contactus', 'http://newscred.com/about/', 'http://newscred.com//www.newscred.com/contact/', 'http://newscred.com/contact/', 'http://nielsen.com/in/en/about-us', 'http://nielsen.com/in/en/contact-us', 'https://www.onespot.com/contact/', 'http://opentext.com/about/contact-us/contact-opentext', 'https://www.pandora.com/about', 'http://pivotshare.com#contact-form', 'http://proquest.com/contact/contact-landing.html', 'http://proquest.com/about', 'https://about.proquest.com/about', 'http://www.realviewdigital.com/free-partica-trial/', 'https://www.realviewdigital.com/about-us/', 'https://www.realviewdigital.com/contact-us/', 'http://info.reprintsdesk.com//info.reprintsdesk.com/about/contact', 'https://info.reprintsdesk.com/about', 'https://info.reprintsdesk.com/about/contact', 'http://salesforce.com/in/form/contact/contactme/?d=cta-header-9', 'http://salesforce.com/in/form/contact/contactme/', 'https://www.salesforce.com/in/form/contact/contactme/?d=cta-footer-contact', 'https://www.salesforce.com/in/form/contact/contactme.jsp?d=70130000000EgLr', 'http://go.sap.com/corporate/en.html', 'https://news.sap.com/press-room/press-contacts/', 'http://go.sap.com//www.sap.com/about.html', '//www.sap.com/index.html/registration/contact.html?pageTitle=Home&countryOfOrigin=en_us&refererPagePath=https%3A%2F%2Fwww.sap.com%2Findex.html&refererContentPath=%2Fcontent%2Fsapdx%2Fwebsite%2Fnam%2Fusa%2Fen_us&navTitle=Contact+Form', 'http://go.sap.com//www.sap.com/registration/contact.html?navTitle=Contact+Form', 'https://www.sas.com/en_in/contact/form/register.html', 'https://www.sas.com/en_in/partners/about-our-program.html', 'https://www.sas.com/en_in/navigation/header/global-header/navigation-items/about.html', 'https://www.sas.com/en_in/contact.html', 'http://sdl.com/contact/', 'http://sdl.com/about/', 'http://sitecore.net/company/contact-us', 'https://www.shift7digital.com/about-us/', 'https://www.shift7digital.com/contact-us/', 'https://www.sizmek.com/about/', 'https://www.skyword.com/about-us/', 'https://www.skyword.com/contact-us/', 'http://smartling.com/resources/101', 'http://smartling.com/about-us', 'http://smartling.com/contact-us', 'http://splunk.com/en_us/about-splunk/contact-us.html#tabs/tab_parsys_tabs_CustomerSupport_4', 'http://splunk.com/en_us/about-splunk.html', 'http://splunk.com/en_us/ask-an-expert.html?expertCode=sales', 'http://splunk.com/en_us/about-splunk/contact-us.html', 'https://www.spotify.com/in/about-us/contact/', 'https://www.spotify.com/in/legal/privacy-policy/#s3', 'http://syncfusion.com/company/contact-us', 'http://syncfusion.com/support/directtrac/incidents/newincident', 'http://syncfusion.com/company/about-us', 'https://sysomos.com/about/', 'http://sysomos.com/contact/', 'https://sysomos.com/contact/', 'https://tapclicks.com/about-us/', 'https://tapclicks.com/contact-us/', 'http://terminalfour.com/about-us/', 'http://terminalfour.com/about-us/contact-us/', 'https://www.webtrends.com/about-us/', 'https://www.webtrends.com/about-us/contact-us/', 'https://www.welocalize.com/contact/', 'http://wistia.com/about', 'http://wistia.com/support/contact', 'https://www.zoominsoftware.com/about-us/', 'https://www.zoominsoftware.com/company/about-us/', 'https://www.zoominsoftware.com/contact-us/', 'http://zumobi.com/about/', 'http://zumobi.com/contact/']
    for url in contacts:
        if(get_location(get_webpage_text(get_webpage(url)))==None or get_location(get_webpage_text(get_webpage(url)))== []):
            logging.error(url)
        else:
            print(get_location(get_webpage_text(get_webpage(url))))