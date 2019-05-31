
# =============================================================================
# 
#                   This Script scrap all historical OHLC data from investing.com
# 
# 
# 
# 
# =============================================================================


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import threading


def investing_scrap( data,start,end):
    chrome = r"chromedriver"
    driver = webdriver.Chrome(executable_path = chrome)
    driver.implicitly_wait(60)
    df=data
    for i in range(start,end):
        
        driver.get(df.iloc[i]['historical'])
        print(i)
        if i == start:
            time.sleep(120)
        wait = WebDriverWait(driver, 5)
        time.sleep(20)
        try:
            e1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.float_lang_base_2.historicDate')))
            e1.click()
    
        except:
            e1 = driver.find_element_by_css_selector('.float_lang_base_2.historicDate')
            e1.click()
    
    
        driver.find_element_by_xpath("//*[@id='startDate']").clear()
        driver.find_element_by_xpath("//*[@id='startDate']").send_keys("01/01/2019")
        time.sleep(1)
        driver.find_element_by_css_selector('.newBtn.Arrow.LightGray.float_lang_base_2').click()
        time.sleep(10)
        #download

        try:
            e2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.newBtn.LightGray.downloadBlueIcon.js-download-data')))
            e2.click()
    
        except:
            e2 = driver.find_element_by_css_selector('.newBtn.LightGray.downloadBlueIcon.js-download-data')
            e2.click()


if __name__=="__main__":    
    df = pd.read_pickle(r"/Users/siuhongnai/Desktop/WQD7005 - Data Mining/WQD180055_Milestone1/df.pkl")
    t1 = threading.Thread(target= investing_scrap,args=(df,0,150))
    t2 = threading.Thread(target= investing_scrap,args=(df,151,300))
    t3 = threading.Thread(target= investing_scrap,args=(df,301,450))
    t4 = threading.Thread(target= investing_scrap,args=(df,451,600))
    t5 = threading.Thread(target= investing_scrap,args=(df,601,750))
    t6 = threading.Thread(target= investing_scrap,args=(df,751,len(df)))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
