import requests as req
from bs4 import BeautifulSoup
import logging, json
# import usaddress

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
    addcoLk = []
    comp = get_list(html)
    for i in comp:
        try:
            res = req.get(i[1])
            soup = BeautifulSoup(res.text, 'html.parser')
            for j in soup.find_all('a', href=True):
                if ("Contact" in str(j)):
                    if ("http" not in str(j.get('href'))):
                        addcoLk.append(list([i[0],i[1] + str(j.get('href'))]))
                    else:
                        addcoLk.append(list([i[0],str(j.get('href'))]))
                elif ("About" in str(j)):
                    if ("http" not in str(j.get('href'))):
                        addcoLk.append(list([i[0],i[1] + str(j.get('href'))]))
                    else:
                        addcoLk.append(list([i[0],str(j.get('href'))]))
        except req.exceptions.RequestException as e:
            logging.error(e)
        
    new_addctL = []
    for elem in addcoLk:
        if elem not in new_addctL:
            new_addctL.append(elem)
    addcoLk = new_addctL
    return addcoLk

def get_location(text):
    if(text != None):
        import re
        addr=[]
        regs = ["(^[0-9]{2,4} .*\n.*[0-9]{2,5}.*\n.*\n)","(^\s[0-9]{2,4} .*\n.*[0-9]{2,5}.*\n.*\n)","(^[0-9]{2,4} .*\n.*\n.*\nUnited States)","(^[0-9]{2,4} .*[0-9]{5})"]
        for rg in regs:
            x = re.findall(rg, str(text),flags = re.M)
            x = list(dict.fromkeys(x))
            add = "".join(x)
            addr.append(add)
        while("" in addr) : 
            addr.remove("")
         
        return addr
    else:
        return None

def save_to_json(filename,json_dict):
    json_object = json.dumps(json_dict, indent = 4)
    with open(filename, "w") as outfile: 
        outfile.write(json_object)



if __name__ == "__main__":
    wbp = get_webpage(
        "http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm")
    # print(wbp)
    # wbpt = get_webpage_text(wbp)
    # print(wbpt)
    lists = get_list(wbp)
    # print(lists)
    contacts = get_contact_page_link(wbp)
    # print(contacts)
    
    # ctL = [['Acquia, Inc', 'http://acquia.com/about-us'], ['Acquia, Inc', 'http://acquia.com/about-us/contact'], ['Acquia, Inc', 'http://acquia.com/blog/migration-security-and-more-we-answer-your-burning-questions-about-drupal-9'], ['Acquire Media', 'http://acquiremedia.com/aboutus/'], ['Acquire Media', 'http://acquiremedia.com/contactus/'], ['Act-On Software, Inc.', 'http://act-on.com/contact-us/'], ['Act-On Software, Inc.', 'http://act-on.com/why-act-on/our-story/'], ['Act-On Software, Inc.', 'https://act-on.com/contact-us/'], ['Apple, Inc.', 'http://apple.com/contact/'], ['Aptara, Inc.', 'http://aptaracorp.com/about-aptara/overview'], ['Aquafadas', 'https://www.aquafadas.com/about-us/'], ['Aquafadas', 'https://www.aquafadas.com/contact-us/'], ['Aquafadas', 'http://aquafadas.com/contact-us/'], ['Aquafadas', 'https://global.rakuten.com/corp/about/'], ['Aria Systems, Inc.', 'https://www.ariasystems.com/contact-us/'], ['Aria Systems, Inc.', 'http://ariasystems.com/contact-us/'], ['Atex', 'https://www.atex.com/atex/contact-us/'], ['Atex', 'https://www.atex.com/atex/about-us/'], ['Atex', 'http://atex.com/atex/contact-us/'], ['Attivio', 'http://attivio.com/solutions/customer-support-search'], ['Attivio', 'http://attivio.com/company/about-attivio'], ['Attivio', 'http://attivio.com/contact'], ['Attivio', 'http://attivio.com/contact?utm_lead_source=OrganicSearch-SEO'], ['Atypon Systems, Inc.', 'https://www.atypon.com/about-us/'], ['Atypon Systems, Inc.', 'https://www.atypon.com/contact/'], ['Atypon Systems, Inc.', 'http://atypon.com/contact'], ['Automattic, Inc.', 'http://automattic.com/about/'], ['Automattic, Inc.', 'http://automattic.com/contact/'], ['Brightcove, Inc.', 'http://brightcove.com/en/company/about'], ['Brightcove, Inc.', 'http://brightcove.com/en/contact-us'], ['Brightcove, Inc.', 'https://info.brightcove.com/live-streaming-global?cid=70130000000jfgr&pid=7011O0000038d2e'], ['Brightcove, Inc.', 'https://help.brightcove.com/en/contact/create'], ['Ceros, Inc.', 'https://www.ceros.com/about/meet-the-team/'], ['Ceros, Inc.', 'https://www.ceros.com/about/contact/'], ['Cision US, Inc.', 'http://cision.com/us/contact-us'], ['Cision US, Inc.', 'http://cision.com/us/contact-us/'], ['Cision US, Inc.', 'http://cision.com/us/about/?nav_location=footer'], ['Cision US, Inc.', 'http://cision.com/us/contact-us/?nav_location=footer'], ['Cloudera, Inc.', 'http://cloudera.com/about.html'], ['Cloudera, Inc.', 'http://cloudera.comtel:18887891488'], ['Cloudera, Inc.', 'http://cloudera.com/contact-sales.html'], ['Cloudera, Inc.', 'http://cloudera.com/contact-us.html'], ['Cloudwords, Inc.', 'https://www.cloudwords.com/about-cloudwords'], ['Cloudwords, Inc.', 'https://www.cloudwords.com/contactus'], ['COGNITIVESCALE', 'http://cognitivescale.com/contact/'], ['COGNITIVESCALE', 'http://cognitivescale.com/about/'], ['Contentful', 'http://contentful.com/contact/sales/'], ['Contentful', 'http://contentful.com/about-us/'], ['Contentful', 'http://contentful.com/contact/'], ['ConvertMedia', 'http://convertmedia.comjavascript:;'], 
    # ['ConvertMedia', 'http://convertmedia.com/contact'], ['CoreMedia AG', 'http://coremedia.com/en/about/contact'], ['Crafter Software Corp.', 'http://craftersoftware.com#'], ['Crafter Software Corp.', 'http://craftersoftware.com/about/contact'], ['Crownpeak Technology', 'http://crownpeak.com/about/contact-us'], ['CSOFT International Ltd.', 'http://csoftintl.com/contact-us/'], ['CSOFT International Ltd.', 'https://www.csoftintl.com/contact-us/'], ['DNN Corp.', 'https://www.dnnsoftware.com/about'], ['DNN Corp.', 'https://www.dnnsoftware.com/about/contact-dnn'], ['DNN Corp.', 'http://dnnsoftware.com/About/Resources/Whitepapers'], ['DNN Corp.', 'http://dnnsoftware.com/about'], ['DNN Corp.', 'http://dnnsoftware.com/about/contact-dnn'], ['EBSCO Industries, Inc.', 'http://ebsco.com/contact'], ['EBSCO Industries, Inc.', 'http://ebsco.com/about'], ['Elsevier', 'https://www.elsevier.com/en-in/about'], ['Elsevier', 'http://elsevier.com#footer-661370'], ['Elsevier', 'https://service.elsevier.com/app/overview/elsevier'], ['Episerver', 'http://episerver.com/company'], ['Episerver', 'http://episerver.com/contact-us'], ['Frame.io, Inc.', 'http://frame.iomailto:support@frame.io'], ['Google', 'http://google.com/intl/en/about.html'], ['Hippo B.V.', 'http://onehippo.com#'], ['Hippo B.V.', 'http://onehippo.com/en/about/our-story'], ['Hippo B.V.', 'http://onehippo.com/en/about/contact-us'], ['Hippo B.V.', 'http://onehippo.com'], ['Hootsuite Media, Inc.', 'https://hootsuite.com/about/contact-us'], ['Hootsuite Media, Inc.', 'https://hootsuite.com/about'], ['HubSpot, Inc.', 'http://hubspot.com//offers.hubspot.com/contact-sales'], ['HubSpot, Inc.', 'http://hubspot.com//www.hubspot.com/our-story'], ['HubSpot, Inc.', 'http://hubspot.com//www.hubspot.com/company/contact'], ['HubSpot, Inc.', 'https://help.hubspot.com/'], ['Impelsys', 'https://www.impelsys.com/about-us/'], ['Impelsys', 'https://www.impelsys.com/contact-us/'], ['Kentico Software', 'http://kentico.com/we-are-kentico'], ['Kentico Software', 'http://kentico.com/contact'], ['Krux Digital, Inc.', 'https://help.salesforce.com/home'], ['Krux Digital, Inc.', 'http://krux.com/company/contact-us/'], ['Krux Digital, Inc.', 'https://www.salesforce.com/company/contact-us/?d=cta-header-9'], ['Krux Digital, Inc.', 'http://krux.com/company/contact-us/?d=cta-header-9'], ['Krux Digital, Inc.', 'https://www.salesforce.com/form/contact/marketingcloud_contactme.jsp?d=70130000000lzZ9'], ['Lingotek', 'http://lingotek.com/company'], ['Lingotek', 'http://lingotek.com/contact'], ['Lingotek', 'https://www.olark.com/site/5763-147-10-7373/contact'], ['LinkedIn', 'https://about.linkedin.com/?trk=homepage-basic_directory_aboutUrl'], ['LinkedIn', 'https://press.linkedin.com/about-linkedin?trk=homepage-basic_footer-about'], ['Lionbridge', 'http://lionbridge.com/who-we-are/#about-us'], ['Lionbridge', 'http://lionbridge.com/get-in-touch/'], ['MadCap Software, Inc.', 'https://www.madcapsoftware.com/contact-us/'], ['MadCap Software, Inc.', 'https://www.madcapsoftware.com/support/contact-options.aspx'], ['MadCap Software, Inc.', 'https://www.madcapsoftware.com/customers/customer-success/'], ['MadCap Software, Inc.', 'https://www.madcapsoftware.com/current-promotions/'], ['MadCap Software, Inc.', 'http://madcapsoftware.com/products/'], ['MadCap Software, Inc.', 'http://madcapsoftware.com/solutions/'], ['MadCap Software, Inc.', 'https://www.madcapsoftware.com/company/about-us/'], ['Netflix', 'https://help.netflix.com/contactus'], ['NewsCred', 'http://newscred.com/about/'], ['NewsCred', 'http://newscred.com//www.newscred.com/contact/'], ['NewsCred', 'http://newscred.com/contact/'], ['The Nielsen Co.', 'http://nielsen.com/in/en/about-us'], ['The Nielsen Co.', 'http://nielsen.com/in/en/contact-us'], ['OneSpot', 'https://www.onespot.com/contact/'], ['OpenText Corp.', 'http://opentext.com/about/contact-us/contact-opentext'], ['Pandora Media, Inc.', 'https://www.pandora.com/about'], ['Pivotshare', 'http://pivotshare.com#contact-form'], ['ProQuest, LLC', 'http://proquest.com/contact/contact-landing.html'], ['ProQuest, LLC', 'http://proquest.com/about'], ['ProQuest, LLC', 'https://about.proquest.com/about'], ['Realview', 'http://www.realviewdigital.com/free-partica-trial/'], ['Realview', 'https://www.realviewdigital.com/about-us/'], ['Realview', 'https://www.realviewdigital.com/contact-us/'], ['Reprints Desk, Inc.', 'http://info.reprintsdesk.com//info.reprintsdesk.com/about/contact'], ['Reprints Desk, Inc.', 'https://info.reprintsdesk.com/about'], ['Reprints Desk, Inc.', 'https://info.reprintsdesk.com/about/contact'], ['Salesforce.com, Inc.', 'http://salesforce.com/in/form/contact/contactme/?d=cta-header-9'], ['Salesforce.com, Inc.', 'https://help.salesforce.com/home'], ['Salesforce.com, Inc.', 'http://salesforce.com/in/form/contact/contactme/'], ['Salesforce.com, Inc.', 'https://www.salesforce.com/in/form/contact/contactme/?d=cta-footer-contact'], ['Salesforce.com, Inc.', 'https://www.salesforce.com/in/form/contact/contactme.jsp?d=70130000000EgLr'], ['SAP', 'http://go.sap.com/corporate/en.html'], ['SAP', 'https://news.sap.com/press-room/press-contacts/'], ['SAP', 'http://go.sap.com//www.sap.com/about.html'], ['SAP', '//www.sap.com/index.html/registration/contact.html?pageTitle=Home&countryOfOrigin=en_us&refererPagePath=https%3A%2F%2Fwww.sap.com%2Findex.html&refererContentPath=%2Fcontent%2Fsapdx%2Fwebsite%2Fnam%2Fusa%2Fen_us&navTitle=Contact+Form'], ['SAP', 'http://go.sap.com//www.sap.com/registration/contact.html?navTitle=Contact+Form'], ['SAS Institute, Inc.', 'https://www.sas.com/en_in/contact/form/register.html'], ['SAS Institute, Inc.', 'https://www.sas.com/en_in/partners/about-our-program.html'], ['SAS Institute, Inc.', 'https://www.sas.com/en_in/navigation/header/global-header/navigation-items/about.html'], ['SAS Institute, Inc.', 'https://www.sas.com/en_in/contact.html'], ['SDL PLC', 'http://sdl.com/contact/'], ['SDL PLC', 'http://sdl.com/about/'], ['Sitecore Corp. AS', 'http://sitecore.net/company/contact-us'], ['Siteworx, LLC', 'https://www.shift7digital.com/about-us/'], ['Siteworx, LLC', 'https://www.shift7digital.com/contact-us/'], ['Sizmek, Inc.', 'https://www.sizmek.com/about/'], ['Skyword, Inc.', 'https://www.skyword.com/about-us/'], ['Skyword, Inc.', 'https://www.skyword.com/contact-us/'], ['Smartling, Inc.', 'http://smartling.com/resources/101'], ['Smartling, Inc.', 'http://smartling.com/about-us'], ['Smartling, Inc.', 'http://smartling.com/contact-us'], ['Splunk, Inc.', 'http://splunk.com/en_us/about-splunk/contact-us.html#tabs/tab_parsys_tabs_CustomerSupport_4'], ['Splunk, Inc.', 'http://splunk.com/en_us/about-splunk.html'], ['Splunk, Inc.', 'http://splunk.com/en_us/ask-an-expert.html?expertCode=sales'], ['Splunk, Inc.', 'http://splunk.com/en_us/about-splunk/contact-us.html'], ['Spotify AB', 'https://www.spotify.com/in/about-us/contact/'], ['Spotify AB', 'https://www.spotify.com/in/legal/privacy-policy/#s3'], ['Syncfusion, Inc.', 'http://syncfusion.com/company/contact-us'], ['Syncfusion, Inc.', 'http://syncfusion.com/support/directtrac/incidents/newincident'], ['Syncfusion, Inc.', 'http://syncfusion.com/company/about-us'], ['SYSOMOS', 'https://sysomos.com/about/'], ['SYSOMOS', 'http://sysomos.com/contact/'], ['SYSOMOS', 'https://sysomos.com/contact/'], ['TapClicks', 'https://tapclicks.com/about-us/'], ['TapClicks', 'https://tapclicks.com/contact-us/'], ['TERMINALFOUR, Inc.', 'http://terminalfour.com/about-us/'], ['TERMINALFOUR, Inc.', 'http://terminalfour.com/about-us/contact-us/'], ['Webtrends', 'https://www.webtrends.com/about-us/'], ['Webtrends', 'https://www.webtrends.com/about-us/contact-us/'], ['welocalize', 'https://www.welocalize.com/contact/'], ['Wistia, Inc.', 'http://wistia.com/about'], ['Wistia, Inc.', 'http://wistia.com/support/contact'], ['Zoomin', 'https://www.zoominsoftware.com/about-us/'], ['Zoomin', 'https://www.zoominsoftware.com/company/about-us/'], ['Zoomin', 'https://www.zoominsoftware.com/contact-us/'], ['ZUMOBI', 'http://zumobi.com/about/'], ['ZUMOBI', 'http://zumobi.com/contact/']]
    
    loc = []
    for url in contacts:
        if(get_location(get_webpage_text(get_webpage(url[1])))==None or get_location(get_webpage_text(get_webpage(url[1])))== []):
            logging.error(url[1])
        else:
            loc.append(list([url[0],get_location(get_webpage_text(get_webpage(url[1])))[0]]))
    new_loc = []
    for elem in loc:
        if elem not in new_loc:
            new_loc.append(elem)
    loc = new_loc

    # loc = [['Acquia, Inc', '600 Congress Ave\nAustin, TX 78701\nUnited States\n53 State Street, 10th Floor\nBoston, MA 02109\nUnited States\n1120 NW Couch St. Suite 550\nPortland, OR 97209\nUnited States\n451 El Camino\nReal Suite 235\nSanta Clara, CA 95050\n1775 Tyson’s Blvd\nMcLean, VA 22102\nUnited States\n310 Edward St\nBrisbane City QLD 4000\nAustralia\n53 State Street, 10th Floor\nBoston, MA 02109\xa0888-922-7842\nContact Us\n'], ['Acquia, Inc', '53 State Street, 10th Floor\nBoston,\xa0MA\xa002109\nUnited States\n600 Congress Ave\nAustin, TX 78701\nUnited States\n53 State Street, 10th Floor\nBoston, MA 02109\nUnited States\n1120 NW Couch St. Suite 550\nPortland, OR 97209\nUnited States\n451 El Camino\nReal Suite 235\nSanta Clara, CA 95050\n1775 Tyson’s Blvd\nMcLean, VA 22102\nUnited States\n310 Edward St\nBrisbane City QLD 4000\nAustralia\n53 State Street, 10th Floor\nBoston, MA 02109\xa0888-922-7842\nContact Us\n'], ['Acquia, Inc', '53 State Street, 10th Floor\nBoston, MA 02109\xa0888-922-7842\nContact Us\n'], ['Act-On Software, Inc.', '121 SW Morrison St.Suite 1600Portland, OR 97204'], ['Aria Systems, Inc.', '100 Pine Street, Suite 2450 San Francisco, CA 94111600 Reed Road, Suite 302 Broomall, PA 19008'], ['Automattic, Inc.', '60 29th Street\xa0#343\nSan Francisco, CA 94110\nUnited States of America\n'], ['Brightcove, Inc.', '84 Theobalds Road\nLondon WC1X 8NL+44 207 148 6450 telSeattle601 Union Street\nSuite 1601\n'], ['Ceros, Inc.', "2019 Crain's Fast 50 \r\n2019 Inc. 5000 List \r\n2018 Inc. 5000 List \r\n"], ['Cloudwords, Inc.', '201 California Street, Suite 1350San Francisco, CA 94111'], ['COGNITIVESCALE', '9500 Arboretum Blvd, L-1\nAUSTIN, TX 78759\n855.505.5001\n'], ['CoreMedia AG', '1001 N. 19th Street, Suite 1200Arlington, VA 22209+1.703.945.10791111 Broadway, 3rd FloorOakland, CA 94607'], ['Crafter Software Corp.', '1800 Alexander Bell DriveSuite 400Reston, VA 20191'], ['DNN Corp.', '\t401 Congress Ave, Suite 2650\n\tAustin, TX 78701, USA\n\n'], ['EBSCO Industries, Inc.', '10 Estes Street, Ipswich, MA 01938\nPhone: (978) 356-6500\nToll-Free (USA & Canada): (800) 653-2726\n'], ['Impelsys', '116 West 23rd Street,\nSuite 500, New York, NY 10011, USA\nTel: +1 212 239 4138, Fax: +1 917 591 9536,\n'], ['Kentico Software', '15 Constitution Dr., Suite 2G\nBedford, NH 03110\nUnited States\n83 Mount St, Level 4\nNorth Sydney, NSW 2060\nAustralia\n'], ['Krux Digital, Inc.', 
    # '21 - 200 employees\n201 - 10,000 employees\n10,001+ employees\n'], ['Lionbridge', '1050 Winter Street, Suite 2300\nWaltham, MA 02451\n(World Headquarters)\n3535 Factoria Boulevard SE\nSuite 300\nBellevue, WA 98006\n423 N Ancestor Place #180\nBoise, ID 83704\n\n225 West Washington Street, Suite 2200\nChicago IL 60606\n\n1917 McKinley Avenue\nColumbus, IN 47201\n\n259 West 30th Street\n11th Floor\nNew York, NY 10001\n3100 De La Cruz Blvd\nSuite 101\nSanta Clara, CA 95054\n220 Montgomery Street\nSuite 605\nSan Francisco, CA 94104\n126 York Street\nSuite 500\nOttawa, Ontario K1N 5T5\n333 Caoxi Road North, Suite B-1106\nXuhui, Shanghai, P.R.China 200030\n\n1605 Sangam-dong\nMapo-gu, Seoul 121-795\n\n191 Silom Road\nSilom Bangrak, Bangkok 10500\n\n45 Allée des Ormes – BP 1200\n06254 Mougins, France\n\n'], ['MadCap Software, Inc.', '9191 Towne Centre Drive, Suite 150 San Diego, California\r\n                                92122\r\n                            \n'], ['NewsCred', '400 W South Boulder Rd\nSuite 2500 c/o NewsCred\nLafayette, CO 80026\n'], ['OneSpot', '401 Congress Avenue, Suite 2650Austin, TX 78701\n(800) 285-3806\nSupport\n'], ['Realview', '100 Barangaroo Avenue\r\nSydney, NSW 2000 Australia\n\n'], ['Salesforce.com, Inc.', '15 - 100 employees\n101 - 500 employees\n501 - 1500 employees\n'], ['Sitecore Corp. AS', '101 California Street \r\n              Floor 16 \r\n\r\n200 South Tyron Street\r\n              Suite 850\r\n\r\n7950 Legacy Drive\r\n              Suite #400\r\n\r\n1750 Elm St.\r\n              11th Floor\r\n\r\n'], ['Splunk, Inc.', '270 Brannan Street\nSan Francisco, CA 94107\nemail: Map and Directions\n500 Santana Row\nSan Jose, CA 95128\nphone: 408.753.1900\n5360 Legacy Place, Ste 250\nPlano, TX 75024\nphone: 972.244.8806\n1730 Minor Avenue, Suite 900\nSeattle, WA 98101\nphone: 206.430.5200\n7900 Tysons One Place, Suite 1100\nMcLean, VA 22102\nphone: 703.206.6400\n270 Brannan Street\nSan Francisco, CA 94107\ninfo@splunk.com\n1118 CN Schiphol\nphone: +31 20 7991773\n\n18 National Circuit\nBarton, ACT 2600\nAustralia\n511 Young Dong St\nGangnam-gu, Seoul 06164\nRepublic of Korea\n'], ['TapClicks', '701 Edgewater DriveSuite #330Wakefield, MA 01880'], ['Zoomin', '150 West 28th St\n17th\xa0floor\nNew York, NY 10001\n'], ['Zoomin', '\xa0150 West 28th St, 17th Floor\nNew York, NY 10001\n\xa0\xa0646.216.8876\n'], ['ZUMOBI', '100 Best Companies to Work For 2013\niab mixx Awards 2013 Gold Winner\nThe Smarties\n']]

    jd={}
    for i in lists:
        jds = []
        for itms in loc:
            if(i[0]==itms[0]):
                lc = itms[1].replace("\n", " ").replace("\r"," ").replace("\xa0"," ").replace("\t"," ").replace("\u2019"," ")
                if("States" in lc):
                    x = lc.split("States ")
                    y = []
                    for ij in x:
                        y.append(ij+"States ")
                    jds.append(y)
                elif("email: Map and Directions" in lc):
                    x = lc.split("email: Map and Directions")
                    for k in x:
                        jds.append(k)
                else:
                    jds.append(lc)
        if(jds != []):
            jd[i[0]]=jds

    sjson = save_to_json("sample.json",jd)
    print(sjson)