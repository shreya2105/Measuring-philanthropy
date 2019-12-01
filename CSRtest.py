from bs4 import BeautifulSoup as bs
link = "http://www.csr.gov.in/CSR/companyprofile.php?year=FY 2015-16&CIN=L17110MH1973PLC019786"
s = link.replace("http://www.csr.gov.in/CSR/companyprofile.php?year=FY 2015-16&CIN=", "")
print(s) 