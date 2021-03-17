#!/usr/bin/ python3
from .db.db import DbConnection

query_list = ['SET SQL_SAFE_UPDATES=0',
              "UPDATE newsapi_n SET publishedAt = DATE_SUB(publishedAt, INTERVAL 8 hour) WHERE publishedAt > CURRENT_TIMESTAMP() and siteName = 'news.cts.com.tw'",
              "UPDATE newsapi_n SET publishedAt = DATE_SUB(publishedAt, INTERVAL 8 hour) WHERE publishedAt > CURRENT_TIMESTAMP() and siteName = 'scmp.com'"]


if __name__ == "__main__":
    db = DbConnection("", False)
    for query_line in query_list:
        db.update(query_line)