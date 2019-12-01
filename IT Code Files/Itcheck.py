from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from IT_NGO_Scrapes_module import sqlite_interface
from datetime import datetime
import time
null=None

processDB = sqlite_interface()

driver = webdriver.Safari()
wait = WebDriverWait(driver, 10)
driver.get("http://www.incometaxindia.gov.in/Pages/utilities/exempted-institutions.aspx")


call_names = {"Address": "Address", "State": "State", "City": "City", "Chief Commissioner of Income Tax Cadre Controlling Authority (CCIT- CCA) / DGIT (Exemptions)":"CCIT_DGIT_Exemptions", "Chief Commissioner of Income Tax (CCIT)":"CCIT", "Commissioner of Income Tax (CIT)": "CIT","Approved under Section": "Approved_under_Section", "Date of Order (DD/MM/YYYY)": "Date_of_order", "Date of Withdrawal/Cancellation (DD/MM/YYYY)":"Date_of_withdrawal", "Date of Expiry (DD/MM/YYYY)": "Date_of_Expiry", "Remarks": "Remarks"}

while True:
    for elem in wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"faq-sub-content exempted-result"))):
        listofIDstoScrape = []
        
        name = elem.find_elements_by_class_name("fc-blue fquph")
        pancard = elem.find_elements_by_class_name("pan-id")
        details = driver.find_elements_by_class_name("exempted-detail")
        page_number =  driver.find_element_by_class_name("act_search_header").text
        print (page_number)
        
        for n, p, key in zip(name, pancard, details):
            main_list = {"Name": (n.text.replace(p.text,'')), "Pancard": p.text}
            for elem_li in key.find_elements_by_tag_name("li"):
                main_list[call_names [elem_li.find_element_by_tag_name('strong').text]] = elem_li.find_element_by_tag_name('span').text
                
            check = processDB.checkID(main_list["Name"], main_list["Approved_under_Section"])
            if check is True:

                listofIDstoScrape.append(main_list)
            #print (main_list)
        
        processDB.AppendToDB(listofIDstoScrape)
        #processDB.closeConnection()    

        
        wait.until(EC.presence_of_element_located((By.ID, "ctl00_SPWebPartManager1_g_d6877ff2_42a8_4804_8802_6d49230dae8a_ctl00_imgbtnNext"))).click()
        wait.until(EC.staleness_of(elem))
        
        time.sleep(3)            
            
#driver.quit()