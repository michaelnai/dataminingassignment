import bs4 as bs
import urllib.request
import pandas as pd
import spacy
from spacy import displacy
from collections import Counter
import numpy as np
import time
import datetime as dt
from interruptingcow import timeout





headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
reg_url = "https:XXXXOOOO"


for j in range(0,100):
    if j%20==0:
        edge_home = "https://www.theedgemarkets.com/categories/corporate?page="
        df_texts = pd.DataFrame(columns=["texts"])
        df_dates = pd.DataFrame(columns=["dates"])
        k=j+20

        print("===================================================================================================")
        print("Iterating from page {} to page {}".format(str(j),str(k)))
        print("===================================================================================================\n")

        while True:

            for i in range(j,k):

                time.sleep(1)
                start = time.time()
                print("---------------------------- Page {} ----------------------------".format(str(i)))
                print("Process initializing")
                the_edge = edge_home + str(i)
                print("Current url: {}\n".format(the_edge))

                print("Requesting URL...")

                try:
                    with timeout(5, exception=RuntimeError):
                            req = urllib.request.Request(url=the_edge, headers=headers)
                            print("Successfully requested URL\n")
                            pass

                except RuntimeError:
                    print("Process took too long, restarting...")
                    break


                print("Opening URL...")
                try:
                    with timeout(5, exception=RuntimeError):
                        html = urllib.request.urlopen(req).read()
                        print("Successfully open URL and registered HTML object\n")
                        pass

                except RuntimeError:
                    print("Process took too long, restarting...")
                    break

                print("Parsing BeautifulSoup Object...")
                edge = bs.BeautifulSoup(html,'lxml')
                print("Successfully Parsed BS object\n")

                print("Start Scrapping...\n")


                for url in edge.find_all("div",attrs={"class":"views-field views-field-title"}):
                   texts = url.text.strip()
                   df_texts=df_texts.append({"texts":texts},ignore_index=True)

                for dates in edge.find_all("div",attrs={"class":"views-field views-field-created"}):
                    df_dates = df_dates.append({"dates":dates.text.strip()},ignore_index=True)

                stop = time.time()
                print("Time taken: {} seconds\n".format(str(stop-start)))


            else:
                break


        df_dates[['date','time']] = df_dates['dates'].str.split('|',expand=True)
        df_dates.drop(columns=["dates"], inplace = True)
        df = pd.concat([df_texts,df_dates],axis=1)

        df = pd.DataFrame(df)


        datemin = df['date'].min()
        datemax = df['date'].max()
        df.to_csv("{}_{}the_edge_title.csv".format(datemin,datemax))
        print("Successfully got news headline from [{}] to [{}]".format(str(datemin),str(datemax)))

    else:
        pass
        

        



