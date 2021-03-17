from twitterscraper import query_tweets
import json
import datetime

if __name__ == '__main__':
    search_query = "WuhanVirus OR 2019nCoV OR Coronavirus OR WuhanCoronavirus OR coronaviruses OR coronavirusoutbreak OR coronavirus OR Covid-19 OR COVID-19 OR ChineseCoronavirus OR Coronaoutbreak"
    filename = "corona_twitter.json"
    #filename = "{}.json".format(username)
    tD = twitterData(search_query, filename)
    tD.query()



class twitterData:
        def __init__ (self, search_query: str, filename: str):
            self.search_query = search_query
            self.filename = filename
        def query(self):
            tweets = query_tweets(query=self.search_query, begindate=datetime.date(2019, 12, 30), enddate=datetime.date(2020, 1, 27))
            print("Found: {} tweets".format(len(tweets)))
            j = []
            for t in tweets:
                t.timestamp = t.timestamp.isoformat()
                print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
                j.append(t.__dict__)
            with open(self.filename, "w") as f:
                f.write(json.dumps(j))
