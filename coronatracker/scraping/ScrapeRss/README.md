# Run scrape_rss.py

## Install dependencies

Recommended to use `python3.8`, I faced issue with `python3.6` as the `datetime` library behaves differently.

```shell
pip3 install -r requirements.txt
```

## Update database credentials

Enter database credentials to `db.json` in `coronatracker/scraping/` directory. Format can be seen in `db.json.example`.

## Steps to run `scrape_rss.py`

Run for testing to get all latest news output in `./data/\<lang\>/output.jsonl`

```python
python ScrapeRss/scrape_rss.py -d -a
```

- d flag: debug mode, only writes to file
- a flag: all, skip cache, don't write to cache

Run to update database on test and production table (use `-v` flag for log messages)

```python
python ScrapeRss/scrape_rss.py --table [ TABLE NAME ]
```

## Some tips

- *Script seems to be hang*
  - when running the script initially, there might be a lot of URLs to go through
  - you can debug by checking the latest log

  - ```shell
    ### check the approximate how many items left in the queue
    tail -f $(ls logs | tail -n 1) | grep --line-buffered  "===>"
    ### or stream the whole log file
    tail -f $(ls logs | tail -n 1)
    ```

  - if the logs are indeed stuck, please file an issue and tag samueljklee@gmail.com with the log file.
