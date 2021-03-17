from twitterscraper import query_tweets
import json
import datetime


# root - We are trying to aggregate seperate tweets and there data members
class Tweet:
  """
  This class is can store a single tweet in its data members.
  """

  # Initializes the data members of the Tweet when the instance is made
  def __init__(self, username, tweet_id, hashtags, links, timestamp, text):
    self.username = username
    self.tweet_id = tweet_id
    self.hashtags = hashtags
    self.links = links
    self.timestamp = timestamp
    self.text = text
    
  # Getter functions to acces the data members of the tweets
  def get_username(self):
    return self.username

  def get_tweet_id(self):
    return self.tweet_id

  def get_hashtags():
    return self.hashtags

  def get_links():
    return self.links

  def get_timestamp():
    return self.timestamp

  def get_text():
    return self.text




if __init__: "__main__":

  search_query = "WuhanVirus OR 2019nCoV OR Coronavirus OR WuhanCoronavirus OR coronaviruses OR coronavirusoutbreak OR coronavirus OR Covid-19 OR COVID-19 OR ChineseCoronavirus OR Coronaoutbreak"
  filename = "corona_twitter.json"
  #filename = "{}.json".format(username)

  tweets = query_tweets(query=search_query, begindate=datetime.date(2019, 12, 30), enddate=datetime.date(2020, 1, 27))
  print("Found: {} tweets".format(len(tweets)))
  # Found: 7 tweets

  # List of Tweet objects
  list_tweets = []
  j = []
  for t in tweets:
    t.timestamp = t.timestamp.isoformat()


    # Make an instance of the Tweet class and pass the data of the current tweet
    new_tweet = Tweet(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text)

    # Add the new Tweet instance into the list of tweets
    list_tweets.append(new_tweet)

    print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
    j.append(t.__dict__)

    
  with open(filename, "w") as f:
      f.write(json.dumps(j))



