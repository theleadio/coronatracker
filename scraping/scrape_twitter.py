from twitterscraper import query_tweets
import json
import datetime


# This class acts as an aggregate root
# It allows entry to the specific data points from objects within the domain of the aggregate (The list of tweets)

class Tweet:
    def __init__(self, username, tweet_id, hashtags, links, timestamp, text):
        self.username = username
        self.tweet_id = tweet_id
        self.hashtags = hashtags
        self.links = links
        self.timestamp = timestamp
        self.text = text


if __name__ == '__main__':
    search_query = "WuhanVirus OR 2019nCoV OR Coronavirus OR WuhanCoronavirus OR coronaviruses OR coronavirusoutbreak OR coronavirus OR Covid-19 OR COVID-19 OR ChineseCoronavirus OR Coronaoutbreak"
    filename = "corona_twitter.json"

    tweets = query_tweets(query=search_query, begindate=datetime.date(2019, 12, 30), enddate=datetime.date(2020, 1, 27))
    print("Found: {} tweets".format(len(tweets)))

    j = []
    # tweet_list is the aggregate which contains a cluster of domain objects (Tweet objects)
    tweet_list = []

    for t in tweets:
        t.timestamp = t.timestamp.isoformat()
        
        # Create new Tweet object from current data points and append it to the end of the tweet list
        tweet_list.append( Tweet(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text) )
        
        print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
        j.append(t.__dict__)


    with open(filename, "w") as f:
        f.write(json.dumps(j))
