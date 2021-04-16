from twitterscraper import query_tweets
import json
import datetime

if __name__ == '__main__':
    search_query = "WuhanVirus OR 2019nCoV OR Coronavirus OR WuhanCoronavirus OR coronaviruses OR coronavirusoutbreak OR coronavirus OR Covid-19 OR COVID-19 OR ChineseCoronavirus OR Coronaoutbreak"
    filename = "corona_twitter.json"
    #filename = "{}.json".format(username)

    tweets = query_tweets(query=search_query, begindate=datetime.date(2019, 12, 30), enddate=datetime.date(2020, 1, 27))
    print("Found: {} tweets".format(len(tweets)))

    # Now will call the adapter pattern to compile and log the tweets 
    j = []
    target = Target()
    twitter_request(target)
    
    # for t in tweets:
    #     t.timestamp = t.timestamp.isoformat()
    #     print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
    #     j.append(t.__dict__)

    # with open(filename, "w") as f:
    #     f.write(json.dumps(j))


class Target:
    # Domain specific interface used by the client's code (compile the tweets into a json)
    def compile_tweets(self, tweets) -> str:
        j = []
        for t in tweets:
            t.timestamp = t.timestamp.isoformat()
            print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
            j.append(t.__dict__)
        return j


class Adaptee:
    # Adaptee for functions that call the adapter, but can't use its function
    def request(self, tweets) -> str:
        pass


class Adapter(Target, Adaptee):
    # Adapter for other functions that are calling the compile tweets, but for a different purpose
    def request(self, tweets) -> str:
        j = self.compile_tweets(tweets)
        return j


def twitter_request(target: 'Target') -> None:
    # Runs the code for any class that follows the target's interface
    j = target.compile_tweets(tweets)
    with open(filename, "w") as f:
        f.write(json.dumps(j))
