from twitterscraper import query_tweets
import json
import datetime
from abc import ABCMeta, abstractstaticmethod

class ITwitterBuilder(metaclass=ABCMeta):
    """The Builder Interface"""

@abstractstaticmethod
def set_username(self, value);
    """Set the unsername"""

@abstractstaticmethod
def set_tweet_id(self, value):
    """Set the tweet_id"""

@abstractstaticmethod
def set_hashtag(self, value)
    """Set the hashtag"""

@abstractstaticmethod
def set_links(self, value)
    """Set the links"""

@abstractstaticmethod
    def set_timestamp(self, value)
    """set the timestamp"""

@abstractstaticmethod
    def set_text(self,value)
    """set the text"""

@abstractstaticmethod
    def get_result(self):
        """return the tweet"""

class TwitterBuilder(ITwitterBuilder):
    """The concrete Builder"""

    def _init__(self):
        self.product = Twitter()

    def set_username(self, value):
        self.product.username = value
        return self

    def set_tweet_id(self, value):
        self.product.tweet_id = value
        return self

    def set_hashtag(self, value):
        self.product.hashtag = value
        return self

    def set_links (self, value):
        self.product.links = value
        return self
    
    def set_timestamp(self, value):
        self.product.links = value
        return self
    
    def set_text(self, value):
        self.product.text = value
        return self

    def get_result(self):
        return self.product
    
class Twitter():
    """The Product"""

    def _init_(self, username= " ", tweet=" ", hashtag=" ", links=" ", timestamp = 0, text=" ")
    self.username = username
    self.tweet = tweet
    self.hashtag = hashtag
    self.links = links
    self.timestamp = timestamp
    self.text = text



class Director:
    """Director building a representation"""
    @staticmethod
    def construct()
        return TwitterBuilder()\
            .set_username()\
            .set_tweet_id()
            .set_hashtag()\
            .set_links()\
            .set_timestamp()\
            .set_text()\
            .get_result()\

if _name_ == "_main_":
    msg = Director.construct()

    print(msg)

if __name__ == '__main__':
    search_query = "WuhanVirus OR 2019nCoV OR Coronavirus OR WuhanCoronavirus OR coronaviruses OR coronavirusoutbreak OR coronavirus OR Covid-19 OR COVID-19 OR ChineseCoronavirus OR Coronaoutbreak"
    filename = "corona_twitter.json"
    #filename = "{}.json".format(username)

    tweets = query_tweets(query=search_query, begindate=datetime.date(2019, 12, 30), enddate=datetime.date(2020, 1, 27))
    print("Found: {} tweets".format(len(tweets)))

    j = []
    for t in tweets:
        t.timestamp = t.timestamp.isoformat()
        print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
        j.append(t.__dict__)

    with open(filename, "w") as f:
        f.write(json.dumps(j))
