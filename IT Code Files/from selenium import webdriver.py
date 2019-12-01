from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver = webdriver.Safari()
wait = WebDriverWait(driver, 1)
driver.get("http://www.incometaxindia.gov.in/Pages/utilities/exempted-institutions.aspx")


call_names = {"Address": "Address", "State": "State", "City": "City", "Chief Commissioner of Income Tax Cadre Controlling Authority (CCIT- CCA) / DGIT (Exemptions)":"CCIT_DGIT_Exemptions", "Chief Commissioner of Income Tax (CCIT)":"CCIT", "Commissioner of Income Tax (CIT)": "CIT","Approved under Section": "Approved_under_Section", "Date of Order (DD/MM/YYYY)": "Date_of_order", "Date of Withdrawal/Cancellation (DD/MM/YYYY)":"Date_of_withdrawal", "Date of Expiry (DD/MM/YYYY)": "Date_of_Expiry", "Remarks": "Remarks"}


while True:

    for elem in wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"faq-sub-content exempted-result"))):

        listofIDstoScrape = []

        name = elem.find_elements_by_class_name("fc-blue fquph")
        pancard = elem.find_elements_by_class_name("pan-id")
        details = driver.find_elements_by_class_name("exempted-detail")
        for i in details:
            pan = i.text

        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'li')))

        for n, p, key in zip(name, pancard, details):
            main_list = {"Name": (n.text.replace(p.text,'')), "Pancard": p.text}

            for elem_li in key.find_elements_by_tag_name("li"):
                main_list[call_names [elem_li.find_element_by_tag_name('strong').text]] = elem_li.find_element_by_tag_name('span').text

            print (main_list)

    try:
        for k in range(2,10):
                myElem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "ctl00_SPWebPartManager1_g_d6877ff2_42a8_4804_8802_6d49230dae8a_ctl00_txtPageNumber")))
                myElem.send_keys(str(k))
                myElem.send_keys(Keys.RETURN)


        print ("Page is ready!")
        break

    except TimeoutException:
            print ("Loading took too much time!")