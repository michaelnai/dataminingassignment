import pandas as pd
import datetime as dt

df = pd.read_csv("top3_combined_stock.csv")
df.drop('Unnamed: 0',axis=1,inplace=True)
df['Price Up'] = 0
for index,row in df.iterrows():
    if row['Movement'] == 'Up':
        df.iloc[index,-1] = 1
    else:
        df.iloc[index,-1] = 0
df.drop('Movement',axis=1,inplace=True)
df['Date'] = df['Date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))

klci_df = pd.read_csv('FTSE Malaysia KLCI Historical Data.csv')
klci_df['Date'] = klci_df['Date'].apply(lambda x: dt.datetime.strptime(x, '%b %d, %Y'))
klci_df = klci_df.sort_values('Date', axis=0, ascending=True)
klci_df['Price'] = klci_df['Open'].str.replace(",","")
klci_df['Open'] = klci_df['Open'].str.replace(",","")
klci_df['Open'] = pd.to_numeric(klci_df['Open'])
klci_df['Price'] = pd.to_numeric(klci_df['Price'])
klci_df['Return'] = klci_df['Price'].pct_change()
klci_df = klci_df.loc[klci_df['Date'] >= dt.datetime(2019, 1, 1)]
klci_df = klci_df.loc[klci_df['Date'] <= dt.datetime(2019, 4, 1)]
klci_df.dropna(inplace=True)
klci_df.drop(['Price','Change %','High','Low'],axis=1,inplace=True)
klci_df.columns = ['Date','Open','Volume','Return']
volumes = []
for index,row in klci_df.iterrows():
    if row['Volume'][-1] == "K":
        vol = float(row['Volume'][:-1])*1000
    elif row['Volume'][-1] == "M":
        vol = float(row['Volume'][:-1])*1000000
    elif row['Volume'] == "-":
        vol = 0

    volumes.append(vol)
klci_df['Volume'] = volumes

df = pd.merge(left=df,right=klci_df[['Date','Open','Volume','Return']],left_on='Date',right_on='Date',suffixes=("","_KLCI"))



df.to_csv("top3_combined_stock_binary.csv")
