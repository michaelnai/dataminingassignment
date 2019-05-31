import glob
import os
import pandas as pd
import datetime as dt
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt


def no_news_imputer(df):
    """Observations with no news on the day will be imputed with 0 on polarity and no news on sentiment"""
    for index,row in df.iterrows():
         if np.isnan(row['polarity']):
             df.iloc[index,-1] = 'no news'

         else:
             pass



def plotting_for_stocks(df,stock):
    """Plotting polarity and normalized stock price movement to identify relationship """
    scaler = preprocessing.MinMaxScaler()
    df = df.loc[df['Stock']==str(stock)]
    x = np.array(df['Close'])
    x = x.reshape(-1, 1)
    x_scaled = scaler.fit_transform(x)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(df['Date'], x_scaled, c="green", label=str(stock))
    ax.scatter(df['Date'], df['polarity'], label='Headline Polarity', c='red')
    ax.legend(loc='best')
    ax.plot(df['Date'], np.zeros(shape=(len(df), 1)), ':', c='red')
    ax.title.set_text("2019 Q1 - Price and News Polarity of " + str(stock))
    ax.set_xlim(df['Date'].min(), df['Date'].max())
    ax.set_xlabel('Date')
    ax.set_ylabel('Normalized Stock Price and Polarity')
    ax.set_xticklabels(labels=df['Date'],rotation=90)
    for label in ax.get_xaxis().get_ticklabels()[::2]:
        label.set_visible(False)
    plt.show()

def penny_stock_filter(df):

    avg_close_df = df.groupby('code')['Close'].mean()
    avg_close_df = df.reset_index()
    penny_stock_code_list = []

    for row in range(len(avg_close_df)):
        if avg_close_df['Close'][row] <= 1:
            penny_stock_code_list.append(avg_close_df['code'][row])
        else:
            pass
    penny_stock_df = df[df['code'].isin(penny_stock_code_list)]
    penny_stock_df.reset_index(inplace=True, drop=True)
    return penny_stock_df



