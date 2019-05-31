import glob
import os
import pandas as pd
import datetime as dt
import numpy as np
from sklearn import preprocessing
import matplotlib as mpl
import matplotlib.pyplot as plt
# ================================================= Import ================================================= #

path = r'https://github.com/michaelnai/dataminingassignment/tree/master/Milestone4/stock_data_2019_Q1/'
pickle_df = pd.read_pickle(r'https://github.com/michaelnai/dataminingassignment/blob/master/Milestone4/df.pkl')
code_df = pickle_df[['code','name']]


for index, row in code_df.iterrows():
    row[1] = row [1].replace("(","").replace(")","").replace("\t","")[-4:]

files = glob.glob(os.path.join(path, "*.csv"))

stock_name = []
for file in files:
    df = pd.read_csv(file)
    df = df.dropna()
    df['Date'] = df['Date'].apply(lambda x: dt.datetime.strptime(x, '%b %d, %Y'))
    df = df.loc[df['Date'] >= dt.datetime(2019, 1, 1)]
    df = df.loc[df['Date'] <= dt.datetime(2019, 4, 1)]
    df = df.sort_values('Date', axis=0, ascending = True )
    df['stock'] = file
    df['Return'] = df['Price'].pct_change()
    stock_name.append(df)



# ================================================= Cleaning ================================================= #

stock_df = pd.concat(stock_name, axis=0, ignore_index=True)
stock_df.rename(columns = {"Vol." : "Volume", "Price" : "Close"},inplace = True)
stock_df['Stock'] = stock_df['stock'].str.replace(path,"").str.replace(" ", "").str.replace('%20',"").str.replace('.csv',"").str.replace("HistoricalData","")
stock_df.drop(['Change %','stock'] ,axis=1,inplace=True)
stock_df = pd.merge(stock_df,code_df,left_on='Stock',right_on='name',how='outer')
stock_df.drop('name', axis=1, inplace=True)
stock_df['code'] = stock_df['code'].apply('{0:0>4}'.format)
stock_df.isna().sum()

set(stock_df.loc[stock_df['code'].isna()]['Stock'])
for index,row in stock_df.iterrows():
    if row['Stock'] == 'DUOP':
        stock_df.iloc[index, -1] = '7148'

    elif row['Stock'] == 'IMPI':
        stock_df.iloc[index, -1] = '7243'

    elif row['Stock'] == 'MERI':
        stock_df.iloc[index, -1] = '5040'

    elif row['Stock'] == 'MSCM':
        stock_df.iloc[index, -1] = '0041'

    elif row['Stock'] == 'RED':
        stock_df.iloc[index, -1] = '5270'


stock_df = stock_df.dropna()

preferred_index = []
for index,row in stock_df.iterrows():
    if len(row['Stock'])==5:
        idx = index
        preferred_index.append(idx)
    else:
        pass


stock_df = stock_df.drop(preferred_index)

volumes = []
for index,row in stock_df.iterrows():
    if row['Volume'][-1] == "K":
        vol = float(row['Volume'][:-1])*1000
    elif row['Volume'][-1] == "M":
        vol = float(row['Volume'][:-1])*1000000
    elif row['Volume'] == "-":
        vol = 0

    volumes.append(vol)


stock_df['Volume'] = volumes

incomplete_idx_list = []
for index, row in stock_df.iterrows():
    if len(stock_df.loc[stock_df['Stock']==row['Stock']])<31:
        incomplete_idx = index
        incomplete_idx_list.append(incomplete_idx)
    else:
        pass

stock_df = stock_df.drop(incomplete_idx_list)


stock_df.reset_index(inplace=True, drop=True)

# ================================================= Pick Stock ================================================= #

def sharpe_ratio(x):
    """Compute Sharpe Ratio for all the stocks"""
    return x.mean()/x.std()

sharpe = stock_df.groupby('Stock')['Return'].apply(lambda x: sharpe_ratio(x))

for stock in sharpe.index[sharpe.isna()]:
    sharpe[stock] = stock_df.loc[stock_df['Stock'] == stock]['Return'].mean()

sharpe.sort_values(inplace = True, ascending = False)
sharpe = sharpe.to_frame()
sharpe.columns = ['Sharpe Ratio']
sharpe = sharpe.reset_index()

def get_top_n_stock(df,n):
    """Get the list of n stocks with the highest sharpe ratio"""
    top_stocks = []
    for index,row in df.head(n).iterrows():
        stock = row[0]
        top_stocks.append(stock)
    return top_stocks

stock_df['Movement'] = ""
for index, row in stock_df.iterrows():
    if row['Return']<0:
        stock_df.iloc[index, -1] = "Down"
    elif row['Return']>0:
        stock_df.iloc[index, -1] = "Up"
    else:
        stock_df.iloc[index, -1] = "No"

print("Stocks with the highest sharpe ratio:" + str(get_top_n_stock(sharpe,3)))

bimb_stock_df = stock_df.loc[stock_df['Stock'].str.contains(get_top_n_stock(sharpe,5)[0])]
kjcs_stock_df = stock_df.loc[stock_df['Stock'].str.contains(get_top_n_stock(sharpe,5)[1])]
cbms_stock_df = stock_df.loc[stock_df['Stock'].str.contains(get_top_n_stock(sharpe,5)[2])]


sentiment_df = pd.read_csv('https://github.com/michaelnai/dataminingassignment/blob/master/Milestone4/milestone4_cleaned_data/cleaned_headlines.csv')
sentiment_df.drop('Unnamed: 0', axis=1, inplace = True )
sentiment_df.columns
sentiment_df['date'] = sentiment_df['date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))


bimb_news_df = sentiment_df.loc[sentiment_df['texts'].str.contains('BIMB|Bank Islam|Takaful')]
kjcs_news_df = sentiment_df.loc[sentiment_df['texts'].str.contains('KJCS|Kian Joo')]
cbms_news_df = sentiment_df.loc[sentiment_df['texts'].str.contains('Carlsberg|CBMS')]


bimb_combined_df = pd.merge(left = bimb_stock_df,right= bimb_news_df, left_on = 'Date', right_on='date',how='outer')
bimb_combined_cleaned_df = bimb_combined_df.drop(['date','time','texts'],axis=1)
kjcs_combined_df = pd.merge(left = kjcs_stock_df,right= kjcs_news_df, left_on = 'Date', right_on='date',how='outer')
kjcs_combined_cleaned_df = kjcs_combined_df.drop(['date','time','texts'],axis=1)
cbms_combined_df = pd.merge(left = cbms_stock_df,right= cbms_news_df, left_on = 'Date', right_on='date',how='outer')
cbms_combined_cleaned_df = cbms_combined_df.drop(['date','time','texts'],axis=1)


def clean_top_stocks_combined_df(df):
    """Observations with no news on the day will be imputed with 0 on polarity and no news on sentiment"""
    for index,row in df.iterrows():
         if np.isnan(row['polarity']):
             df.iloc[index,-1] = 'no news'
             df.iloc[index,-2] = 0

         else:
             pass

clean_top_stocks_combined_df(bimb_combined_cleaned_df)
clean_top_stocks_combined_df(kjcs_combined_cleaned_df)
clean_top_stocks_combined_df(cbms_combined_cleaned_df)

bimb_combined_cleaned_df.dropna(thresh=3, inplace=True)
kjcs_combined_cleaned_df.dropna(thresh=3, inplace=True)
cbms_combined_cleaned_df.dropna(thresh=3, inplace=True)

top_3_combined_stock_df = pd.concat([bimb_combined_cleaned_df,kjcs_combined_cleaned_df,cbms_combined_cleaned_df],ignore_index=True)
top_3_combined_stock_df.to_csv("top3_combined_stock.csv")

# ================================================= Plotting ================================================= #


def plotting_for_stocks(df):
    """Plotting polarity and normalized stock price movement to identify relationship """
    scaler = preprocessing.MinMaxScaler()
    x = np.array(df['Close'])
    x = x.reshape(-1, 1)
    x_scaled = scaler.fit_transform(x)

    plt.plot(df['Date'], x_scaled, c="green", label=df['Stock'][0])
    plt.scatter(df['Date'], df['polarity'], label='Headline Polarity', c='red')
    plt.legend(loc='best')
    plt.plot(df['Date'], np.zeros(shape=(len(df), 1)), ':', c='red')
    plt.title("2019 Q1 - Price and News Polarity of " + str(df['Stock'][0]))
    plt.xlim(df['Date'].min(), df['Date'].max())
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.ylabel('Normalized Stock Price and Polarity')
    plt.show()

plotting_for_stocks(bimb_combined_df)
plotting_for_stocks(kjcs_combined_df)
plotting_for_stocks(cbms_combined_df)



