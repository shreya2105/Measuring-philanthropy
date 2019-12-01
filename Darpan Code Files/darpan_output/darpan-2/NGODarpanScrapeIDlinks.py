from bs4 import BeautifulSoup
import requests
import json
import time

def get_states(url):
    links = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    for link in soup.find_all("a", class_="bluelink11px"):
        links.append(link.get('href')) 
    return links

def get_pages(statepagelink):
	k_100 = statepagelink +"?per_page=100"
	print (k_100)
	sub_link = requests.get(k_100)
	soup = BeautifulSoup(sub_link.text, 'lxml')
	#print (soup)
	linksdata=[]
	ul = soup.find('ul',  class_="pagination")

	base_url_for_this_state=statepagelink[0:-1]
	last_page=1
	if ul is not None:
		pageNos = [a['href'] for a in ul.find_all('a') if a.text in ['>','Last']]
		last_page=pageNos[-1].replace("?per_page=100","").split("/")[-1]
	



	state_page_list=[]
	for i in range(1,int(last_page)+1):
		this_url=base_url_for_this_state+str(i)+"?per_page=100"
		state_page_list.append(this_url)

	return(state_page_list)

		
def getIDsForEachState(link):
	linksdata=[]
	textdata =[]
	get_page = requests.get(link)
	soup = BeautifulSoup(get_page.content, 'lxml')
	first_div = soup.find ('div',  class_ = "ibox-content")
	get_tr = first_div.find_all('a', onclick=True)
	for eachID in get_tr:
		link=eachID['onclick']
		text = eachID.text
		ID=''.join([num for num in link])
		linksdata.append(ID)
		textdata.append(text)
	return linksdata, textdata
	




url = "https://ngodarpan.gov.in/index.php/home/statewise"
state_url = get_states(url)

# state_url=["https://ngodarpan.gov.in/index.php/home/statewise_ngo/31/35/1","https://ngodarpan.gov.in/index.php/home/statewise_ngo/1852/23/1","https://ngodarpan.gov.in/index.php/home/statewise_ngo/145/12/1"]

for url in state_url:

	AllLinksForEachState=get_pages(url)
	with open("NewIDList.txt","a+") as IDListfile:
		for eachlink in AllLinksForEachState:
			print(url,eachlink)
			linkpage=getIDsForEachState(eachlink)
			IDListfile.write('\n'.join(linkpage))





