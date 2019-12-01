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

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


retries=3,
backoff_factor=0.3

retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor
        )
adapter = HTTPAdapter(max_retries=retry)



processDB = sqlite_interface()


counter=1
with open("DarpanIDList.txt") as IDfile:
	for line in IDfile:
		counter+=1
		line=str(line.replace("\n",""))
		check = processDB.checkID(line)

		if check is True:
			time.sleep(3)
			s=requests.Session()
			s.headers['User-agent']='Mozilla/5.0 (Windows NT 6.1)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36'
			s.mount('https://', adapter)
			print(counter,line)
			r = s.get("https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf")
			my_dict=json.loads(r.text)
			s.headers["X-Requested-With"]="XMLHttpRequest"
			csrf_token=my_dict['csrf_token']
			data = dict (id = str(line), csrf_test_name = csrf_token)
			p = s.post("https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info", data=data)
			NGO_info = (json.loads(p.text))
			NGO_info['digitalID']=line
			processDB.AppendToDB([NGO_info])
			
		else:
			print (counter,line,"already in DB")

processDB.closeConnection()
