from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os

import pandas as pd
import datetime as dt
import time

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
chrome = os.path.join(PROJECT_ROOT, "chromedriver")
MY_EXPORT_ROOT = "/Users/zeroyan/Documents/_Master/workspace/wqd7005/"
the_star_link = "https://www.thestar.com.my/business/marketwatch/stock-list/?"
MY_STORE_DIR_DAILY = "Daily-test"
MY_STORE_DIR_SECTOR = "sector-test"

title = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
         "W", "X", "Y", "Z", "0-9"]
# title1 = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
main = ["main_healthcare", 'main_finance', 'main_indprod', 'main_energy', 'main_telcomedia'
    , 'main_plantation', 'main_technology', 'main_consumer', 'main_transport',
        'main_property', 'main_construction', 'main_specialpurposeact', 'main_utilities',
        'main_reits', 'main_closedfund']
ace = ['ace_healthcare', 'ace_finance', 'ace_indprod', 'ace_technology', 'ace_consumer', 'ace_telcomedia'
    , 'ace_transport', 'ace_construction', 'ace_utilities']
bond = ['bond_finance', 'bond_indprod', 'bond_energy', 'bond_telcomedia', 'bond_property', 'bond_islamic']
warrant = ['warrants_healthcare', 'warrants_finance', 'warrants_telcomedia', 'warrants_indprod', 'warrants_energy',
           'warrants_transport', 'warrants_plantation', 'warrants_consumer', 'warrants_technology', 'warrants_property',
           'warrants_construction', 'warrants_utilities']
etf = ['etf_bond', 'etf_equity', 'etf_commodity']

col_Names = ["idx", "Symbol", "Open", "High", "Low", "Last", "Chg", "%Chg", "Vol ('00)", "Sector"]


class MyCrawler:
    def __init__(self, url):
        self.url = url
        print("Running {}".format(self.url))

    def run(self):
        # self.main(self.url)
        if self.url == "title":
            arr = title
            str_link = "alphabet"
            store_dir = MY_STORE_DIR_DAILY
        elif self.url == "main":
            arr = main
            str_link = "sector"
            store_dir = MY_STORE_DIR_SECTOR + "/main market"
        elif self.url == "ace":
            arr = ace
            str_link = "sector"
            store_dir = MY_STORE_DIR_SECTOR + "/ace"
        elif self.url == "bond":
            arr = bond
            str_link = "sector"
            store_dir = MY_STORE_DIR_SECTOR + "/bond"
        elif self.url == "warrant":
            arr = warrant
            str_link = "sector"
            store_dir = MY_STORE_DIR_SECTOR + "/warrant"
        elif self.url == "etf":
            arr = etf
            str_link = "sector"
            store_dir = MY_STORE_DIR_SECTOR + "/etf"

        self.loop_func(arr, str_link, store_dir)

        return

    def test(self):
        print(self.url)
        if self.url == "etf":
            # temp_file = pd.read_csv(MY_EXPORT_ROOT + MY_STORE_DIR_SECTOR + "/etf/2019-03-03.csv", names=col_Names)
            my_file = MY_EXPORT_ROOT + MY_STORE_DIR_SECTOR + "/etf/2019-03-03.csv"
            cov = pd.read_csv(my_file, sep=',')
            # frame = pd.DataFrame(cov.values, columns=col_Names)
            # frame['sector'] = "xx"
            # frame.to_csv(my_file, sep=",")
            cov['sector'] = "xx"
            cov.to_csv(my_file)
            # print(temp_file.head(5))
        return

    @staticmethod
    def loop_func(arr, str_link, store_dir):
        chromeOptions = webdriver.ChromeOptions()
        # prefs = {'profile.managed_default_content_settings.images': 2, 'disk-cache-size': 4096}
        prefs = {'profile.managed_default_content_settings.images': 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        # driver = webdriver.Chrome(executable_path=chrome)
        driver = webdriver.Chrome(executable_path=chrome, options=chromeOptions)
        temp = the_star_link + str_link + "="
        delay = 20
        df1 = pd.DataFrame()
        # print(format(df1.size))

        for i in arr:
            # time.sleep(5)
            link = temp + i
            driver.get(link)
            # loopidx = 0
            try:
                time.sleep(2)
                table = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'marketwatchtable')))
                df = pd.read_html(table.get_attribute('outerHTML'), header=0)[0]
                # df1 = df1.append(df)
                temp_file_name = MY_EXPORT_ROOT + store_dir + r"/{}.csv".format(dt.datetime.today().strftime('%Y-%m-%d'))

                if str_link != "alphabet":
                    df['sector'] = i

                if not os.path.isfile(temp_file_name):
                    df.to_csv(temp_file_name)
                else:
                    df.to_csv(temp_file_name, header=False, mode='a')
                print("Done {} ".format(i))

            except TimeoutException:
                print("Loading took too much time at this page {}!".format(i))

        # df1.to_csv(
        #     MY_EXPORT_ROOT + store_dir + r"/{}.csv".format(dt.datetime.today().strftime('%Y-%m-%d')))

        driver.close()
        return


# crawler = MyCrawler("title")
# crawler.run()

MyCrawler("title").run()
# MyCrawler("main").run()
# MyCrawler("ace").run()
# MyCrawler("bond").run()
# MyCrawler("warrant").run()
# MyCrawler("etf").run()

# MyCrawler("etf").test()