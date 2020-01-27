from twitter_scraper import get_tweets
import pandas as pd

# selected tag = ['#coronavirus,#Coronaoutbreak,]

res_list = []
result_df = pd.DataFrame()
num_pages = 10

for i in range(1, num_pages+1):
    for tweet in get_tweets('#CoronaVirus', pages=i):
        tweet['time'] = str(tweet['time'])  # convert datetime object to str
        res_list.append(tweet)
