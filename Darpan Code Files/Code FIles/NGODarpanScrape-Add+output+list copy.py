
# coding: utf-8

# In[65]:


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


# In[66]:


processDB = sqlite_interface()


# In[67]:


def get_states(url):
    links = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    for link in soup.find_all("a", class_="bluelink11px"):
        links.append(link.get('href')) 
    return links


# In[68]:


url = "https://ngodarpan.gov.in/index.php/home/statewise"


# In[69]:


#url = "https://ngodarpan.gov.in/index.php/home/statewise_ngo/2569/7/1?per_page=100"
def get_pages():
        url = "https://ngodarpan.gov.in/index.php/home/statewise_ngo/1277/24/1?per_page=100"
        sub_link = requests.get(url)
        soup = BeautifulSoup(sub_link.content, 'lxml')
        ul = soup.find('ul',  class_="pagination")

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
        
        linksdata=[]
        
        for c in page_list:
                    url = "https://ngodarpan.gov.in/index.php/home/statewise_ngo/1277/24/"+str(c)+"?per_page=100"
                    #print(url)
                    get_page = s.get(url)
                    soup = BeautifulSoup(get_page.content, 'lxml')
                    first_div = soup.find ('div',  class_ = "ibox-content")
                    get_tr = first_div.find_all('a', onclick=True)
                    linksdata+=get_tr
                    #ngodata=get_NGOs(get_tr)
        return linksdata


# In[70]:


#stlinks=get_pages()


# In[71]:


#function to store NGO IDs in a list
def get_Ids(stlinks):
    id_list = []
    for ngoinfo in stlinks:
        link=ngoinfo['onclick']
        ID=''.join([num for num in link if num.isdigit()])
        id_list.append(ID)
    return id_list


# In[72]:


#ID=get_Ids(stlinks)


# In[73]:


#ID = '183236','96779','176294']#,
ID=['177309', '97671', '156566', '120504', '17732', '116460', '155281', '155203', '181139', '104506', '162083', '164059','163059','88681','184956','182771','113041','164434','173012','164546','178544','105223','182353']
 
#get_Ids(statelinks)

def get_NGOs(stlinks):
    infolist=[]
    done_Ids = []
    for ID in stlinks:
        r = s.get("https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf")
        s.headers["X-Requested-With"]="XMLHttpRequest"
        my_dict=json.loads(r.text)
        # print (my_dict)
        csrf_token=my_dict['csrf_token']
        data = dict (id = ID, csrf_test_name = csrf_token)
        #print (data)
        p = s.post("https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info", data=data)
        NGO_info = (json.loads(p.text))
        #print (NGO_info)
        NGO_info['digitalID'] = ID
        infolist.append(NGO_info)
        done_Ids.append (ID)
        #print (infolist)
        time.sleep(3)
            
    return infolist


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
#processDB.closeConnection()


# In[57]:


processDB = sqlite_interface()


# In[58]:


from NGO_darpan_support_modules_python3 import sqlite_interface


# In[59]:


processDB = sqlite_interface()


# In[61]:


processDB.closeConnection()


# In[62]:


from NGO_darpan_support_modules_python3 import sqlite_interface


# In[63]:


processDB = sqlite_interface()


# In[64]:


processDB.closeConnection()


# In[74]:


processDB.closeConnection()


# In[75]:


from NGO_darpan_support_modules_python3 import sqlite_interface


# In[76]:


processDB.closeConnection()

