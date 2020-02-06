"""
    Created by: Edmund Hee
    Email: edmund.hee05@gmail.com
"""
# from .Firebase.firebase_model import FireStoreModel
from bs4 import BeautifulSoup
import db_connector
import requests
import re
import json
import datetime
import pytz
import logging

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db_connector.connect()

def parse_date(text, tz=None):
    """
    Parse JSON data to date
    :param text: date in string
    :return: datetime object
    """
    if text == '' or text is None:
        return None

    for fmt in ["%A, %d %b %Y %I:%M %p"]:
        try:
            dt = datetime.datetime.strptime(text, fmt)
            if tz:
                timezone = pytz.timezone(tz)
                dt = timezone.localize(dt)
            else:
                dt = dt.replace(tzinfo=None)
            return dt
        except ValueError:
            pass
    return None


def parse_date_to_string(dt, fmt="%Y-%m-%d %H:%M:%S.%f"):
    """
    Convert date time to string format of %Y-%m-%d %H:%M:%S.%f
    :param datetime: datetime object
    :param fmt: datetime format (default: %Y-%m-%d %H:%M:%S.%f)
    :return: string datetime
    """
    try:
        if dt:
            return dt.strftime(fmt)
        else:
            return None
    except Exception as e:
        logging.error("Error: parse_date_to_string Exception - {}".format(str(e)))
        return None



@app.route('/scrap_the_star')
def scrap_the_star():

    content_list = []

    page_no = 1
    input_counter = 0
    while not content_list or len(content_list) == input_counter:
        print(f"Page No : {page_no}")
        respond = requests.get(f"https://www.thestar.com.my/search?pgno={page_no}&q=coronavirus&qsort=newest&qrec=30")
        respond_bd = BeautifulSoup(respond.content, "html")

        result = respond_bd.find_all("div", {"class":"list-listing"})
        news = [link.a["href"] for link in result]

        img_pattern = re.compile(r'(\{.*?\}),')
        content = {}
        for news_link in news:
            print(news_link)
            res = requests.get(news_link)
            bs = BeautifulSoup(res.content, "html")

            bs_img = bs.find_all("div", {"class": ["story-image", "embeded-image"]})
            bs_author = bs.find_all("p", {"class": "byline"})
            bs_title = bs.find_all("h1")
            bs_content = bs.find_all("div", {"id": "story-body"})
            bs_date = bs.find_all("p", {"class": "date"})
            bs_timestamp = bs.find_all("time", {"class": "timestamp"})

            t = bs_img[0].script

            content["url"] = news_link
            content["title"] = bs_title[0].text.strip()
            if t:
                if img_pattern.findall(str(t)):
                    image_path = json.loads(img_pattern.findall(str(t))[0])['image_path']
                    if image_path:
                        if "https" in image_path:
                            content["urlToImage"] = image_path
                        else:
                            content["urlToImage"] = f"https://apicms.thestar.com.my/{image_path}"
                    else:
                        content["urlToImage"] = ""

            if bs_author:
                content["author"] = bs_author[0].a.text
            else:
                content["author"] = ""

            if bs_content:
                tmp_content = ""
                for item in bs_content:
                    tmp_content = tmp_content + item.text
                content["content"] = tmp_content
            else:
                content["content"] = ""

            content["source"] = "TheStar"

            utc_tz = pytz.timezone("UTC")
            if bs_date and bs_timestamp:
                news_dt = parse_date(f"{bs_date[0].text.strip()} {bs_timestamp[0].text.replace('MYT', '').strip()}", tz="Asia/Kuala_Lumpur")

                if news_dt:
                    news_dt = news_dt.replace(tzinfo=utc_tz)
                    content["publishedAt"] = parse_date_to_string(news_dt)
                else:
                    content["publishedAt"] = ""
            else:
                content["publishedAt"] = ""

            content["description"] = ""
            content["summary"] = ""
            content["accessDateTime"] = parse_date_to_string(datetime.datetime.utcnow())

            if not db_connector.check_news(title=content["title"], source=content["source"]):
                db_connector.insert(content)
                input_counter += 1

            content_list.append(content)

        if len(content_list) == input_counter:
            page_no += 1

        print(f"len(content_list) : {len(content_list)}")
        print(f"input_counter : {input_counter}")

    return jsonify({"news": content_list, "inserted_row": input_counter}), 200


if __name__ == '__main__':
    app.run()
