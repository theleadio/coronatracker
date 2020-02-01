# Run scrape_rss.py

## Install dependencies

```shell
pip3 install -r requirements.txt
```

## Update database credentials

Enter database credentials to `db.json`. Format can be seen in `db.json.example`.

Update your table name to write to in `db_connector.py`. Replace `TEST_TABLE_NAME` with your table name.

## Steps to run `scrape_rss.py`

Run to get all latest news output in `./data/\<lang\>/output.jsonl`

```python
python scrape_rss.py -d -a
```

- d flag: debug mode, only writes to file
- a flag: all, skip cache, don't write to cache

Run to update database on test and production table (use `-v` flag for log messages)

```python
python scrape_rss.py -v # writes to test table
python scrape_rss.py -v -p # writes to production table
```
