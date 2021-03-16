from twitterscraper import query_tweets
import json
import datetime

Class KeywordSearch:
def __init__(self,keyword):
    self.query_search = keyword #Term for twitterscraper to search by


KeywordSearch_1 = KeywordSearch("WuhanVirus")
KeywordSearch_2 = KeywordSearch("2019nCoV")
KeywordSearch_3 = KeywordSearch("Coronavirus")
KeywordSearch_4 = KeywordSearch("WuhanCoronavirus")
KeywordSearch_5 = KeywordSearch("coronaviruses")
KeywordSearch_6 = KeywordSearch("coronavirusoutbreak")
KeywordSearch_7 = KeywordSearch("coronavirus")
KeywordSearch_8 = KeywordSearch("Covid-19")
KeywordSearch_9 = KeywordSearch("COVID-19")
KeywordSearch_10 = KeywordSearch("ChineseCoronavirus")
KeywordSearch_11 = KeywordSearch("Coronaoutbreak")

if __name__ == '__main__':
    #search_query = "WuhanVirus OR 2019nCoV OR Coronavirus OR WuhanCoronavirus OR coronaviruses OR coronavirusoutbreak OR coronavirus OR Covid-19 OR COVID-19 OR ChineseCoronavirus OR Coronaoutbreak"
    filename = "corona_twitter.json"
    #filename = "{}.json".format(username)

    tweets = query_tweets(query=KeywordSearch.keyword, begindate=datetime.date(2019, 12, 30), enddate=datetime.date(2020, 1, 27))
    print("Found: {} tweets".format(len(tweets)))

    j = []
    for t in tweets:
        t.timestamp = t.timestamp.isoformat()
        print("{} {} {} {} {}: {}".format(t.username, t.tweet_id, t.hashtags, t.links, t.timestamp, t.text))
        j.append(t.__dict__)

    with open(filename, "w") as f:
        f.write(json.dumps(j))
