import pandas as pd
from milestone6_toolkit import no_news_imputer, plotting_for_stocks
import numpy as np
import matplotlib.pyplot as plt
from talib import RSI, BBANDS


headlines = pd.read_csv("https://github.com/michaelnai/dataminingassignment/blob/master/Milestone6/milestone6data/headlines_df_m6.csv",index_col=0)
headlines = headlines.rename({'date':'Date'},axis='columns')
headlines_test = pd.read_csv("https://github.com/michaelnai/dataminingassignment/blob/master/Milestone6/milestone6data/headlines_df_m6_test.csv",index_col=0)
headlines_test = headlines_test.rename({'date':'Date'},axis='columns')

headlines = pd.concat([headlines,headlines_test])

stocks = pd.read_csv("https://github.com/michaelnai/dataminingassignment/blob/master/Milestone6/milestone6data/cleaned_stock_data_m6.csv",index_col=0,dtype={'code':'object'})
stocks_test = pd.read_csv("https://github.com/michaelnai/dataminingassignment/blob/master/Milestone6/milestone6data/cleaned_stock_data_m6_test.csv",index_col=0,dtype={'code':'object'})

# Calculate average Sharpe Ratio for each industry and identify the top n industries in terms of Sharpe Ratio
sector_sharpe = stocks.groupby('sector').mean().sort_values('Sharpe Ratio')
def find_top_n_sector(n):
    for i in range(n):
        top_sector_sharpe_name = "|".join(sector_sharpe.index[(-1*n):].to_list())
    return top_sector_sharpe_name

top_5 = find_top_n_sector(5)
top5_sector_stocks = stocks.loc[stocks['sector'].str.contains(top_5)].reset_index(drop=True)
top5_agg = top5_sector_stocks.groupby(['sector','Stock'],as_index=False)['Sharpe Ratio'].max()
top5_agg = top5_agg.groupby('sector').apply(lambda x: x['Stock'][x['Sharpe Ratio'].idxmax()])
portfolio_stocks_list = list(top5_agg)

stocks = top5_sector_stocks.loc[top5_sector_stocks['Stock'].str.contains("|".join(portfolio_stocks_list))].reset_index(drop=True)

#Extract related news

CBMS_headlines = headlines.loc[headlines['texts'].str.contains('Carlsberg|CBMS')]
CBMS_headlines['Stock'] = 'CBMS'
DEHB_headlines = headlines.loc[headlines['texts'].str.contains('DEHB|Dayang')]
DEHB_headlines['Stock'] = 'DEHB'
MYRS_headlines = headlines.loc[headlines['texts'].str.contains('MYRS|Malaysian Resourcer')]
MYRS_headlines['Stock'] = 'MYRS'
RTON_headlines = headlines.loc[headlines['texts'].str.contains('RTON|Redtone')]
RTON_headlines['Stock'] = 'RTON'
MEGA_headlines = headlines.loc[headlines['texts'].str.contains('MEGA|Mega First')]
MEGA_headlines['Stock'] = 'MEGA'
top5_headlines = pd.concat([CBMS_headlines,DEHB_headlines])
top5_headlines = pd.concat([top5_headlines,MYRS_headlines])
top5_headlines = pd.concat([top5_headlines,RTON_headlines])
top5_headlines = pd.concat([top5_headlines,MEGA_headlines])

portfolio_stocks = pd.merge(stocks,top5_headlines.iloc[:,[1,3,4,5]],on=['Stock','Date'],how='outer')
portfolio_stocks_test = pd.merge(stocks_test,top5_headlines.iloc[:,[1,3,4,5]],on=['Stock','Date'],how='outer')

no_news_imputer(portfolio_stocks)
no_news_imputer(portfolio_stocks_test)

portfolio_stocks.dropna(thresh=5,inplace=True)
portfolio_stocks_test.dropna(thresh=5,inplace=True)



# Form a portfolio with one stock from each of the industries
# Visualize Stock Return and News

for stock in portfolio_stocks_list:
    plotting_for_stocks(portfolio_stocks,stock)

# Compute covariance between the portfolio stocks
# Data need to be scaled before computing covariance

stock_df = stocks.sort_values('Date',ascending=True)
stock_df = stock_df.pivot_table('Return',['Date'], 'Stock')
stock_df.fillna(method='ffill',inplace=True)
stock_df.fillna(method='bfill',inplace=True)

cov_df = stock_df.cov()
corr_df = stock_df.corr()

portfolio_corr = corr_df.loc[portfolio_stocks_list,portfolio_stocks_list]
portfolio_cov = cov_df.loc[portfolio_stocks_list,portfolio_stocks_list]
portfolio_stocks_return = stock_df.loc[:,portfolio_stocks_list]

# Stimulate portfolios with different weights
np.random.seed(33)
n_portfolio = 30000
all_weights = np.zeros((n_portfolio, len(portfolio_stocks_return.columns)))
ret_arr = np.zeros(n_portfolio)
vol_arr = np.zeros(n_portfolio)
sharpe_arr = np.zeros(n_portfolio)

for x in range(n_portfolio):
    # Random Weights
    weights = np.array(np.random.random(5))
    weights = weights / np.sum(weights)
    all_weights[x, :] = weights

    # E(return)
    ret_arr[x] = np.sum((portfolio_stocks_return.mean() * weights))

    # E(risk)
    vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(portfolio_stocks_return.cov(), weights)))

    # Sharpe Ratio
    sharpe_arr[x] = ret_arr[x] / vol_arr[x]


# Maximize Portfolio Sharpe Ratio with Linear Programming

from scipy.optimize import minimize

def objecf(weights):
    weights = np.array(weights)
    returns = np.sum(portfolio_stocks_return.mean() * weights)
    volatility = np.sqrt(np.dot(weights.T, np.dot(portfolio_stocks_return.cov(), weights)))
    sr = returns/volatility
    return np.array([returns,volatility,sr])

def min_objecf(weights):
    return objecf(weights)[2]*-1

def weight_sum(weights):
    return np.sum(weights)-1

initial_guess = [0.2,0.2,0.2,0.2,0.2]
bounds = [(0,1),(0,1),(0,1),(0,1),(0,1)]

optimal_result = minimize(min_objecf,initial_guess,method='SLSQP',bounds=bounds, constraints={'type':'eq','fun':weight_sum})

for i,stock in enumerate(portfolio_stocks_list):
    print('{} weightage in portfolio: {}%'.format(stock,optimal_result.x[i]*100))

print('The optimized portfolio sharpe ratio:{}'.format(objecf(optimal_result.x)[2]))

# Plotting Efficient Frontier
def minimize_volatility(weights):
    return objecf(weights)[1]

frontier_x = []
frontier_y = np.linspace(0.004,0.018,200)

for possible_return in frontier_y:
    cons = ({'type': 'eq', 'fun': weight_sum},
            {'type': 'eq', 'fun': lambda w: objecf(w)[0] - possible_return})
    result = minimize(minimize_volatility,initial_guess, method='SLSQP', bounds=bounds, constraints=cons)
    frontier_x.append(result['fun'])

plt.figure(figsize=(12,8))
plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis_r')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Risk')
plt.ylabel('Return')
plt.plot(frontier_x,frontier_y, 'r--', linewidth=3)
plt.title('Portfolio vs Individual Stock')
plt.scatter(objecf(optimal_result.x)[1], objecf(optimal_result.x)[0] ,c='red', s=50)
plt.text(objecf(optimal_result.x)[1],objecf(optimal_result.x)[0],"Optimal",fontsize=12)

for stock in portfolio_stocks_list:
    ret = portfolio_stocks_return[stock].mean()
    stdv = portfolio_stocks_return[stock].std()
    plt.scatter(stdv,ret,marker='x',color='red')
    plt.text(stdv, ret, stock, fontsize=12)

plt.show()

# Let's have a look at the actual statistic of the return of our portfolio in the coming month

actual_portfolio = portfolio_stocks_test.sort_values('Date',ascending=True)
actual_portfolio = actual_portfolio.pivot_table('Return',['Date'], 'Stock')
actual_portfolio.fillna(method='ffill',inplace=True)
actual_portfolio.fillna(method='bfill',inplace=True)

actual_portfolio['PORTFOLIO'] = 0.000

for row in range(len(actual_portfolio)):
    actual_portfolio_list = []
    for i in range(len(portfolio_stocks_list)):

        actual_portfolio_list.append(actual_portfolio[portfolio_stocks_list[i]][row]*optimal_result.x[i])

    actual_portfolio['PORTFOLIO'][row] = float(sum(actual_portfolio_list))

print("Portfolio Return for April is {} %".format(actual_portfolio['PORTFOLIO'].mean()*252/12*100))

# Feature Engineering for Modelling
# RSI is the Relative Strength Index of the stock to determine the condition of overbought and oversold of a stock
# Moving average is the average closing price of a stock in a rolling window

portfolio_stocks['3 Days RSI'] = portfolio_stocks.groupby('Stock')['Close'].apply(lambda x:RSI(x, timeperiod=3))
portfolio_stocks_test['3 Days RSI'] = portfolio_stocks_test.groupby('Stock')['Close'].apply(lambda x:RSI(x, timeperiod=3))

portfolio_stocks['3 Days Moving Average'] = portfolio_stocks.groupby('Stock')['Close'].apply(lambda x:x.rolling(window=3).mean())
portfolio_stocks_test['3 Days Moving Average'] = portfolio_stocks_test.groupby('Stock')['Close'].apply(lambda x:x.rolling(window=3).mean())

portfolio_stocks['polarity']=portfolio_stocks['polarity'].fillna(0)
portfolio_stocks_test['polarity']=portfolio_stocks_test['polarity'].fillna(0)

portfolio_stocks = portfolio_stocks.dropna()
portfolio_stocks_test = portfolio_stocks_test.dropna()

# Train a model with Q1 data, and predict if it will make profit in the upcoming Month
# Then we compare the model accuracy with actual data

from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

train_x = portfolio_stocks.iloc[:,[1,2,3,4,5,7,9,10,11,12,14,16,17]]
train_x = pd.get_dummies(train_x)

test_x = portfolio_stocks_test.iloc[:,[1,2,3,4,5,7,9,10,11,12,14,16,17]]
test_x = pd.get_dummies(test_x)

train_y = portfolio_stocks.iloc[:,13]
test_y = portfolio_stocks_test.iloc[:,13]

model = XGBClassifier(learning_rate=0.8,max_delta_step=0.5,max_depth=6,booster='gbtree',objective='binary:hinge')
model.fit(train_x, train_y)

y_pred = model.predict(test_x)
accuracy = accuracy_score(test_y, y_pred)

print("Predicting April stock price movement...")
print("Model Accuracy: {}".format(accuracy * 100.0))
















