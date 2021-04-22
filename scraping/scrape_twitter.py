from twitterscraper import query_tweets
import json
import datetime

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
        ITERABLE = Iterable(t.text)
        while ITERABLE.has_next():
            ITERABLE.next().check_filter()
        j.append(t.__dict__)

    with open(filename, "w") as f:
        f.write(json.dumps(j))

    class IIterator():
        # Interface for the iterator
        def has_next():
            # returns boolean whether it is at the end of collection or not

        def next():
            # returns next object in collection

    class Iterable(IIterator):
        # Concrete class for the iterator

        def __init__(self, tweet_text):
            self.index = 0
            self.tweet_text = tweet_text
        
        def next(self):
            if self.index < len(self.tweet_text):
                self.index += 1
                return self.tweet_text
            raise Exception("AtEndOfIterator", "Reached the end of iterator")

        def has_next(self):
            return self.index < len(self.tweet_text)

    class Aggregate():
        def check_filter(self):
            for word in self.tweet_text:
                for blacklist_word in self.blacklist:
                    if word === blacklist_word:
                        self.tweet_text.flag = True