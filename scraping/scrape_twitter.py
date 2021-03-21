from twitterscraper import query_tweets
import json
import datetime

class Tweets:
  
  def _init_(self):
    self.tweets = []

  def addTweet(tweet):
    self.tweets.append(tweet)

  def writeTweetsToFile(filename):
    with open(filename, 'w') as file:
        json.dumps(self.tweets, filename)


if _name_ == '_main_':
    search_query = "WuhanVirus OR 2019nCoV OR Coronavirus OR WuhanCoronavirus OR coronaviruses OR coronavirusoutbreak OR coronavirus OR Covid-19 OR COVID-19 OR ChineseCoronavirus OR Coronaoutbreak"
    filename = "corona_twitter.json"
    #filename = "{}.json".format(username)
    rootTweets = Tweets()
    tweets = query_tweets(query=search_query, begindate=datetime.date(2019, 12, 30), enddate=datetime.date(2020, 1, 27))
    print("Found: {} tweets".format(len(tweets)))

    for t in tweets:
        t.timestamp = t.timestamp.isoformat()
        print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
        rootTweets.addTweet(t._dict_)

    rootTweets.writeTweetsToFile(filename)

