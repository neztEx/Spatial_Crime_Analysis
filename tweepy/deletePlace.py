import pandas as pd

df = pd.read_csv('../dataset/tweetsWithSentiment.csv')
df.drop(df.columns[[0,1,2,4,8,9]],axis=1,inplace=True)
print(df.head())
df.to_csv('../dataset/cleanedSentimentTweets.csv')