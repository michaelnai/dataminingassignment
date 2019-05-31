# =============================================================================
#
#                   This script scrap the daily fundamental data of
#                   every listed stock
#
# =============================================================================
import pandas as pd
import bs4 as bs
import urllib.request
import datetime as dt

stock_list = pd.read_pickle(r"C:\Users\Baqar\OneDrive\Desktop\Data Mining\all script\klse_screener.pkl")
stock_fundamental = pd.DataFrame(columns=['Stock', 'Stock Code', 'High', 'Low', 'Volume', '52w', 'ROE', 'P/E', 'EPS',
                                          'DPS', 'DY', 'PTBV', 'RPS', 'PSR', 'Market Cap'])

klse_sceener = "https://www.klsescreener.com/v2/stocks/view/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
reg_url = "https:XXXXOOOO"
failed_list = []

print("Total # stock list => ", len(stock_list[0]))

# my_stock_list = ['0043', '0042', '0041', '0040']
for i in stock_list[0]:
# for i in my_stock_list:
    try:
        print("URL => ", klse_sceener + i)
        req = urllib.request.Request(url=klse_sceener + i, headers=headers)
        html = urllib.request.urlopen(req).read()
        screener = bs.BeautifulSoup(html, 'lxml')
        title = screener.find('title').string.strip()
        table = screener.table
        table_rows = table.find_all('tr')

        rows = []
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i in td]
            rows.append(row)

        stock_fundamental = stock_fundamental.append({'Stock': title,
                                                      'Stock Code': i,
                                                      'High': (rows[0][1]),
                                                      'Low': (rows[1][1]),
                                                      'Volume': rows[2][1],
                                                      '52w': rows[6][1],
                                                      'ROE': (rows[7][1]),
                                                      'P/E': (rows[8][1]),
                                                      'EPS': (rows[9][1]),
                                                      'DPS': (rows[10][1]),
                                                      'DY': rows[11][1],
                                                      'PTBV': (rows[13][1]),
                                                      'RPS': (rows[14][1]),
                                                      'PSR': (rows[15][1]),
                                                      'Market Cap': rows[16][1]}, ignore_index=True)
        print("{} done".format(i))

    except:
        failed_list.append(i)
stock_fundamental.to_csv(r'C:\Users\Baqar\OneDrive\Desktop\Data Mining\all script\Fundamental{}.csv'.format(
    dt.datetime.today().strftime('%Y-%m-%d')))

