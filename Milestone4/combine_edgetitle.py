import glob
import os
import pandas as pd
from datetime import datetime
import numpy as np
from textblob import TextBlob

path = r'https://github.com/michaelnai/dataminingassignment/tree/master/Milestone4/theedge_headlines/'

files = glob.glob(os.path.join(path, "*.csv"))
headlines_list = []

for file in files:
    df = pd.read_csv(file)
    headlines_list.append(df)

headlines = frame = pd.concat(headlines_list, axis=0, ignore_index=True)
headlines.drop('Unnamed: 0',axis=1,inplace=True)
headlines['date'] = headlines['date'].str.strip()
headlines['texts'] = headlines['texts'].str.strip()
headlines['date'] = headlines['date'] + " 2019"
headlines = headlines.loc[headlines['date'].str.contains("Jan|Feb|Mar")]
headlines['date'] = headlines['date'].apply(lambda x: datetime.strptime(x,'%d %b %Y'))
headlines = headlines.drop_duplicates()
headlines = headlines.sort_values(['date','time']).reset_index(drop=True)
polarities = []

for index, row in headlines.iterrows():
    text = row[0]
    obj = TextBlob(text)
    sentiment = obj.sentiment.polarity
    if index%100 == 0:
        print('Polarity computation completed for {} rows '.format(str(index)))
    polarities.append(sentiment)

headlines['polarity'] = polarities


conditions = [
    (headlines['polarity'] > 0),
    (headlines['polarity'] < 0)]
choices = ['positive', 'negative']

headlines['sentiment'] = np.select(conditions, choices, default='neutral')

print((headlines[['polarity','sentiment']]).head())

headlines.to_csv('cleaned_headlines.csv')







