import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


stock_df = pd.read_csv('/Users/siuhongnai/Downloads/stock_compiled.csv',low_memory=False)
stock_df = stock_df.drop(['Unnamed: 0','Change'],axis=1)
stock_df = stock_df[stock_df.code != 52507]
stock_df['Date'] = pd.to_datetime(stock_df.Date)
stock_df = stock_df[stock_df['Date']>=dt.datetime(2018,1,1)]
stock_df = stock_df.drop(['Close', 'Open', 'High', 'Low', 'Volume'],axis=1)
stock_df = stock_df.sort_values('Date',ascending=True)
stock_df = stock_df.pivot_table('Return',['Date'], 'code')
stock_df = stock_df.fillna(method='ffill')

def cleaning_index(file):
    file.columns = ["Date","Close","Open","High","Low","Volume","Change"]
    file['Date'] = pd.to_datetime(file.Date).dt.strftime('%Y-%m-%d')
    file['Close'] = file['Close'].apply(lambda x:float((x.replace(",",""))))
    file['Open'] = file['Open'].apply(lambda x:float((x.replace(",",""))))
    file['Low'] = file['Low'].apply(lambda x:float((x.replace(",",""))))
    file['High'] = file['High'].apply(lambda x:float((x.replace(",",""))))
    return file

index = pd.read_csv(r"/Users/siuhongnai/Desktop/WQD7005 - Data Mining/FTSE Malaysia KLCI Historical Data.csv")
index = cleaning_index(index)
index['Return'] = index['Close'].pct_change()
index = index.sort_values('Date',ascending=True)
index['IndexReturn'] = index['Return']
index = index.drop([ 'Close', 'Open', 'High', 'Low', 'Volume','Change','Return'],axis=1)
index['Date']= pd.to_datetime(index.Date)
index = index[index['Date']>=dt.datetime(2018,1,1)]
index = index[index['Date']<=dt.datetime(2019,3,1)]
index = index.sort_values("Date",ascending=True)
df = pd.merge(index,stock_df,on='Date',how='left').fillna(0)
df = df.set_index('Date')
df_standardized = StandardScaler().fit_transform(df)

cov_df = np.cov(df_standardized)
corr_df = np.corrcoef(df_standardized)

# PCA = EigenVectors of the covariance matrix
eigenvalues ,eigenvectors = np.linalg.eig(cov_df)
print('Eigenvectors \n%s' %eigenvectors)
print('\nEigenvalues \n%s' %eigenvalues)

# Visually confirm that the list is correctly sorted by decreasing eigenvalues
eigenpairs = [(np.abs(eigenvalues[i]), eigenvectors[:,i]) for i in range(len(eigenvalues))]
print('Eigenvalues in descending order:')
for i in eigenpairs:
    print(i[0])

pca = PCA().fit(df_standardized)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance')
plt.show()


pca = PCA(5)
projected = pca.fit_transform(df_standardized)
print("Dimension before PCA: " + str(df_standardized.shape))
print("Dimension after PCA: " + str(projected.shape))

pca = PCA(15)
pca.fit(df_standardized)
X_pca = pca.transform(df_standardized)
X_new = pca.inverse_transform(X_pca)
plt.scatter(df_standardized[:, 0], df_standardized[:, 1], alpha=0.2)
plt.scatter(X_new[:, 0], X_new[:, 1], alpha=0.8)
plt.axis('equal')
plt.show();

