
from twitterscraper import query_tweets
import json
import datetime

# root - We are trying t aggregate all the tweets in a single root 
class Tweets:
  """
  Class for storing all the tweets and make several operations on them.
  """

  # Initializes the tweets list
  def __init__(self):
    self.tweets = []
  
  # Adds the tweet in the tweet list of the instance
  def add_tweet(self,  tweet):
    self.tweets.append(tweet)

  # Returns a list of tweets by a user with some username
  def get_tweets_by_user(self, username):
    user_tweets = []

    # Loop through all the tweets
    for t in self.tweets:
      if t["username"] == username:
        user_tweets.append(t)
    return user_tweets


  # Returns a tweet in diictionary format with the given tweet_id = id, 
  # If the tweet with given Id is not availale then it returns an empty dictionary
  def get_tweet_by_id(self, id):
    for t in self.tweets:
      if t["tweeet_id"] == id:
        return t
    return {}


  # Returns a lsit of tweets which have the given query in its text.
  def tweets_with_query_in_text(self, query):
    user_tweets = []
    for t in self.tweets:
      if query in t["text"]:  
        user_tweets.append(t)
    return user_tweets


  # Returns the count of tweets by some user with the given username
  def count_tweet_by_user(self, username):
    count = 0
    for t in self.tweets:
      if t["username"] = username:
        count += 1
    return count



if __init__: "__main__":

  search_query = "WuhanVirus OR 2019nCoV OR Coronavirus OR WuhanCoronavirus OR coronaviruses OR coronavirusoutbreak OR coronavirus OR Covid-19 OR COVID-19 OR ChineseCoronavirus OR Coronaoutbreak"
  filename = "corona_twitter.json"
  #filename = "{}.json".format(username)

  tweets = query_tweets(query=search_query, begindate=datetime.date(2019, 12, 30), enddate=datetime.date(2020, 1, 27))
  print("Found: {} tweets".format(len(tweets)))

  # Instance of Tweet to make the aggregation of all the tweets in a single root
  root = Tweets()  # root 
  j = []
  for t in tweets:
    t.timestamp = t.timestamp.isoformat()

    # Adding the tweets in the root instance
    root.add_tweet(t)  

    print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
    j.append(t.__dict__)

    
  with open(filename, "w") as f:
    f.write(json.dumps(j))




