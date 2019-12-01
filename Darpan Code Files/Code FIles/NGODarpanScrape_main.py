from bs4 import BeautifulSoup
import requests
s=requests.Session()
s.headers['User-agent']='Mozilla/5.0 (Windows NT 6.1)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36'
import re
import json
import time
from NGO_darpan_support_modules_python3 import sqlite_interface
from datetime import datetime
null=None

processDB = sqlite_interface()

def get_states(url):
    links = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    for link in soup.find_all("a", class_="bluelink11px"):
        links.append(link.get('href')) 
    return links

url = "https://ngodarpan.gov.in/index.php/home/statewise"
state_url = get_states(url)

for s_url in state_url:
    def get_pages():
        url_new = state_url #"https://ngodarpan.gov.in/index.php/home/statewise_ngo/1277/24/1?per_page=100"
        for lin in url_new:
            k_100 = lin +"?per_page=100"
            print (k_100)
            sub_link = requests.get(k_100)
            soup = BeautifulSoup(sub_link.content, 'lxml')
            #print (soup)
            linksdata=[]
            ul = soup.find('ul',  class_="pagination")
            if ul!= null: 
                pages = [li.text for li in ul.select('li')]

                if (pages[-1] == "Last"):
                    pages = [li.text for li in ul.select('li')]
                    last_li_number = len (ul.select('li')) 
                    last_li = [li for li in ul.select ('li')]
                    for i in last_li:
                        if (i.text == 'Last'):
                            pages1 = int(i.find ('a').get('data-ci-pagination-page'))
                else:
                    pages1 = int(sum(c.isdigit() for c in pages))
        
        #print (pages1)
                x1= 1
                x2 = pages1
                page_list = [str(x) for x in range(x1, x2+1)]
        #print (page_list)
                
            
        
                for c in page_list:
                    url = "https://ngodarpan.gov.in/index.php/home/statewise_ngo/1277/24/"+str(c)+"?per_page=100"
                    #print(url)
                    get_page = s.get(url)
                    soup = BeautifulSoup(get_page.content, 'lxml')
                    first_div = soup.find ('div',  class_ = "ibox-content")
                    get_tr = first_div.find_all('a', onclick=True)
                    linksdata+=get_tr
            else:
                #get_page = s.get(url)
                #soup = BeautifulSoup(get_page.content, 'lxml')
                first_div = soup.find ('div',  class_ = "ibox-content")
                get_tr = first_div.find_all('a', onclick=True)
                linksdata+=get_tr
                
                    
            return linksdata


    stlinks=get_pages()


#function to store NGO IDs in a list
    def get_Ids(stlinks):
        id_list = []
        for ngoinfo in stlinks:
            link=ngoinfo['onclick']
            ID=''.join([num for num in link if num.isdigit()])
            id_list.append(ID)
        #print(id_list)
        return id_list

    ID=get_Ids(stlinks)
    print(ID)



    def get_NGOs(ID):
        infolist=[]
        done_Ids = []
        for o in ID:
            r = s.get("https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf")
            s.headers["X-Requested-With"]="XMLHttpRequest"
            my_dict=json.loads(r.text)
            # print (my_dict)
            csrf_token=my_dict['csrf_token']
            data = dict (id = o, csrf_test_name = csrf_token)
            print (data)
            p = s.post("https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info", data=data)
            print (p)
            NGO_info = (json.loads(p.text))
            print (NGO_info)
            NGO_info['digitalID'] = o
            infolist.append(NGO_info)
            done_Ids.append (o)
            print (infolist)
            time.sleep(3)
            
        return infolist

    get_NGOs(ID)





listofIDstoScrape=[]
for i in ID:
    print(i)
    
    check = processDB.checkID(i)
    if check is True:
        listofIDstoScrape.append(i)

dataout = get_NGOs(listofIDstoScrape)


# for item in dataout:
#     print (item)
#     item['digitalID']=int(i)
processDB.AppendToDB(dataout)
processDB.closeConnection()

