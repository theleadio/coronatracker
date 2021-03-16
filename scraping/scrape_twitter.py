from twitterscraper import query_tweets
import json
import datetime


class SearchQuery:
    def __init__(self, query):
        self.query = query


search_queries = SearchQuery(
    "WuhanVirus OR 2019nCoV OR Coronavirus OR WuhanCoronavirus OR coronaviruses OR coronavirusoutbreak OR coronavirus OR Covid-19 OR COVID-19 OR ChineseCoronavirus OR Coronaoutbreak")

if __name__ == '__main__':
    filename = "corona_twitter.json"
    # filename = "{}.json".format(username)

    tweets = query_tweets(query=search_queries, begindate=datetime.date(2019, 12, 30), enddate=datetime.date(2020, 1, 27))
    print("Found: {} tweets".format(len(tweets)))

    j = []
    for t in tweets:
        t.timestamp = t.timestamp.isoformat()
        print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
        j.append(t.__dict__)

    with open(filename, "w") as f:
        f.write(json.dumps(j))
