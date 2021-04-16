from twitterscraper import query_tweets
import json
import datetime

class Username:
    def __init__(self, username):
        self.username = username

class TweetID:
    def __init__(self, tweet_id):
        self.tweet_id = tweet_id

class Hashtags:
    def __init__(self, hashtags):
        self.hashtags.hashtags

class Links:
    def __init__(self, links):
        self.links = links

class Timestamp:
    def __init__(self, timestamp):
        self.timestamp = timestamp

class Text:
    def __init__(self, text):
        self.text = text

class Adapter:
    def __init__(self, obj, adpater_methods):
        self.obj = obj
        self.__dict__.update(adpater_methods)

    def __getattribute__(self, attribute):
        return getattr(self.obj, attribute)

    def original_dict(self):
        return self.obj.__dict__

if __name__ == '__main__':
    search_query = "WuhanVirus OR 2019nCoV OR Coronavirus OR WuhanCoronavirus OR coronaviruses OR coronavirusoutbreak OR coronavirus OR Covid-19 OR COVID-19 OR ChineseCoronavirus OR Coronaoutbreak"
    filename = "corona_twitter.json"
    #filename = "{}.json".format(username)

    tweets = query_tweets(query=search_query, begindate=datetime.date(2019, 12, 30), enddate=datetime.date(2020, 1, 27))
    print("Found: {} tweets".format(len(tweets)))

    j = []
    username = Username()
    tweet_id = TweetID()
    hashtags = Hashtags()
    links = Links()
    timestamp = Timestamp()
    text = Text()

    for t in tweets:
        t.timestamp = t.timestamp.isoformat()
        print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
        j.append(Adapter(username, t.username)
        j.append(Adapter(tweetid, t.tweet_id)
        j.append(Adapter(hashtags, t.hashtags)
        j.append(Adapter(links, t.links)
        j.append(Adapter(timestamp, t.timestamp)
        j.append(Adapter(text, t.text)

    with open(filename, "w") as f:
        f.write(json.dumps(j))
