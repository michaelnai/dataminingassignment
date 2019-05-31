import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
chrome = r"C:\Downloads\chromedriver.exe"
driver = webdriver.Chrome(executable_path = chrome)

pages=[]
B=[]
C=[]
D=[]
E=[]
F=[]
G=[]
for i in range(1,3):
    url = 'http://www.bursamalaysia.com/market/listed-companies/company-announcements/#/?category=all&page=' + str(i)
    pages.append(url)
    
for item in pages:
    driver.get(item)
    time.sleep(5)
    html = driver.page_source
    soup  = BeautifulSoup(html)
    
    table = soup.findAll("table", {'summary':"company announcements", 'class':'bm_center bm_dataTable' })
    for row in table[0].findAll('tr'):
        cells = row.findAll('td')
        cells2 = row.findAll('a')
        for link in row.findAll('a'):
            cells3=link.get('href')
            E.append(cells3)
            F, G = E[::2], E[1::2]
        if len(cells)==4: 
            B.append(cells[1].find(text=True))
            C.append(cells2[0].find(text=True))
            D.append(cells2[1].find(text=True))
            
df=pd.DataFrame({'Annoucement_Date':B, 'Comp_Name':C, 'Title':D, 'Comp_Link':F, 'Ann_Link':G})
df['Comp_Code'] = df['Comp_Link'].str.split('=').str.get(1)

df.to_csv('Annoucement.csv',index=False)