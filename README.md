# nhknews

A simple Python script for downloading news and dictionary files from http://www3.nhk.or.jp/news/easy/index.html.

## How to use

Download all news to the default download directory `nhknews_dump`:

    nhknewsdownloader.py

Limit downloading to news from last 30 days:

    nhknewsdownloader.py -d 30

Limit downloading to news from selected date:

    nhknewsdownloader.py --date 2024-01-01

Options:

`--path` - set download directory

Run tests with:

   pytest --cov=nhknewsdownloader --cov-report html
