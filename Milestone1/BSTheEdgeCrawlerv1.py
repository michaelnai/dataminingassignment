import bs4 as bs
import urllib.request
import pandas as pd

#import time
#from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
#chrome = r"/Users/siuhongnai/Documents/chromedriverpath/chromedriver"
#driver = webdriver.Chrome(executable_path = chrome)

edge_home  = "https://www.theedgemarkets.com/categories/corporate?page="
#edge_links = []

links = []
useful_links = []

df=pd.DataFrame(columns=["links","articles"])
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
reg_url = "https:XXXXOOOO"

for i in range(1,3):
    the_edge=edge_home+str(i)
    req = urllib.request.Request(url=the_edge, headers=headers) 
    html = urllib.request.urlopen(req).read() 
    
    #edge_links.append(the_edge)
    
# for items in edge_links:
#     driver.get(items)
#     time.sleep(6)
#     html = driver.page_source
    edge = bs.BeautifulSoup(html,'lxml') 

    #========================== Scrapped Links================================================


    for url in edge.find_all('a'):
        links.append(url.get('href'))

    for i in range(0,len(links)):
        try:
            if '/article' in links[i]:
                useful_links.append(links[i])

        except:
            pass

    for link in useful_links:

        req = urllib.request.Request("http://www.theedgemarkets.com"+link,headers=headers)
        response = urllib.request.urlopen(req).read()
        article= bs.BeautifulSoup(response,'lxml')
        for paragraph in article.find_all('article', attrs={"class":"node node-article und post post-large blog-single-post"}):
            #articles.append(paragraph.text.strip())
            df=df.append({"links":link,"articles":paragraph.text.strip()},ignore_index=True)
            

df.to_csv("the_edge_articles.csv")

