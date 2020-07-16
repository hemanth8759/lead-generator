import requests as req
from bs4 import BeautifulSoup
import logging, json
import usaddress

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


def json_to_csv_file(json_filename,csv_filename):
    import json 
    import csv
  
    # Opening JSON file and loading the data 
    # into the variable data 
    with open(json_filename) as json_file: 
        data = json.load(json_file)

    # now we will open a file for writing 
    data_file = open(csv_filename, 'w') 
  
    # create the csv writer object 
    csv_writer = csv.writer(data_file)
  
    # Counter variable used for writing  
    # headers to the CSV file 

    for itm in data:
        addr_data = data[itm]
        ct = 0
        if ct == 0:
            headr = list([itm])
            csv_writer.writerow(headr)
            ct += 1
            for emp in addr_data:
                count = 0
                if count == 0: 
  
                    # Writing headers of CSV file 
                    header = emp.keys()
                    csv_writer.writerow(header)
                    count += 1
  
            # Writing data of CSV file 
                csv_writer.writerow(emp.values()) 
  
    data_file.close()
    


if __name__ == "__main__":
    # get_webpage function
    wbp = get_webpage(
        "http://www.econtentmag.com/Articles/Editorial/Feature/The-Top-100-Companies-in-the-Digital-Content-Industry-The-2016-2017-EContent-100-114156.htm")
    # print(wbp)

    # get_webpage_text function
    wbpt = get_webpage_text(wbp)
    # print(wbpt)

    # get_list function
    lists = get_list(wbp)
    # print(lists)

    # get_contact_page_link function
    contacts = get_contact_page_link(wbp)
    # print(contacts)

    
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
    
    jd={}
    for i in lists:
        jds = []
        for itms in loc:
            if(i[0]==itms[0]):
                lc = itms[1].replace("\n", " ").replace("\r"," ").replace("\xa0"," ").replace("\t"," ").replace("\u2019"," ")
                if("States" in lc):
                    x = lc.split("States ")
                    for ij in x:
                        if('employees' not in ij and 'Australia' not in ij and 'France' not in ij and "Korea" not in ij and 'Smarties' not in ij):
                            jds.append(usaddress.parse(ij+"States "))
                elif("email: Map and Directions" in lc):
                    x = lc.split("email: Map and Directions")
                    for k in x:
                        if('employees' not in k and 'Australia' not in k and 'France' not in k and "Korea" not in k and 'Smarties' not in k):
                            jds.append(usaddress.parse(k))
                else:
                    if('employees' not in lc and 'Australia' not in lc and 'France' not in lc and "Korea" not in lc and 'Smarties' not in lc):
                        jds.append(usaddress.parse(lc))
        # if(jds != []):
        #     jd[i[0]]=jds
        arad = []
        for ion in jds:
            darr = []
            adt = {}
            for j in ion:
                if(j[1] != "Recipient" and j[1] != "SubaddressType" and j[1] != "SubaddressIdentifier" and j[1] != "ZipPlus4" and j[1] != "NotAddress" and "(" not in j[0] and "-" not in j[0] and "Support" not in j[0]):
                    adt[j[1]]=j[0]
            darr.append(adt)
            # print(darr)
            for q in darr:
                arad.append(q)
            jd[i[0]]=arad

    jd2 = {}
    for valve in jd:
        # print(jd[valve])
        narrs = []
        for arrval in jd[valve]:
            for n in arrval:
                if(n == "ZipCode"):
                    narrs.append(arrval)
        if(narrs != []):
            jd2[valve]=narrs

    updt_jd={}
    for vl in jd2:
        new_vl = []
        for elem in jd2[vl]:
            if elem not in new_vl:
                new_vl.append(elem)
        updt_jd[vl]=new_vl
    
    
    # save_to_json function
    sjson = save_to_json("sample.json",updt_jd)
    print(sjson)

    # json_to_csv_file function
    csvfl = json_to_csv_file("sample.json","sample.csv")
    print(csvfl)