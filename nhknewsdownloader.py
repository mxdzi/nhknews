#!/usr/bin/env python3.11
"""Download news from https://www3.nhk.or.jp/news/easy/index.html"""
import argparse
import os

import requests
from bs4 import BeautifulSoup
from mako.template import Template
from requests.exceptions import RequestException

__version__ = 1.8


class NHKNewsdl:
    NEWS_URL = "https://www3.nhk.or.jp/news/easy/{news_id}/{news_id}"
    NEWS_HTML_URL = f"{NEWS_URL}.html"
    NEWS_DICT_URL = f"{NEWS_URL}.out.dic"

    def __init__(self, days, save_path, date=None):
        self.days = days
        self.save_path = save_path
        self.date = date

    def download(self):
        news_list = self._get_news_list()
        if news_list:
            os.makedirs(self.save_path, exist_ok=True)
            for date, news in news_list:
                print(f"Saving: {date}")
                os.makedirs(os.path.join(self.save_path, date), exist_ok=True)
                for post in news:
                    self._get_post(post, date)
        else:
            print("Error downloading news!")

    def _get_news_list(self):
        response = requests.get("https://www3.nhk.or.jp/news/easy/news-list.json")
        if response.ok:
            news_list = sorted(response.json()[0].items())
            if self.date:
                return [n for n in news_list if n[0] == self.date]

            limit = -self.days if self.days else None
            return news_list[limit:]
        else:
            return None

    def _get_post(self, post, date):
        print(f"Saving:\t\tNews {post['top_priority_number']}", end='')
        url_news = self.NEWS_HTML_URL.format(news_id=post['news_id'])
        url_dict = self.NEWS_DICT_URL.format(news_id=post['news_id'])

        file_name = os.path.join(self.save_path, date, str(post['top_priority_number']))
        file_html = file_name + '.html'
        file_dic = file_name + '.dic.js'

        try:
            response_html = requests.get(url_news)
            response_html.raise_for_status()
            response_html.encoding = 'utf-8'

            response_dict = requests.get(url_dict)
            response_dict.raise_for_status()
            response_dict.encoding = 'utf-8'

            soup = BeautifulSoup(response_html.text, "html.parser")
            article = soup.find('div', id='js-article-body')
            parsed_html = self._prepare_html(article, post)

            self._write_file(file_html, parsed_html)
            print(" html ", end='')
            self._write_file(file_dic, response_dict.text)
            print("dic")

        except RequestException as err:
            print(" ERR ", err, end='\n')

    @staticmethod
    def _prepare_html(article, news):
        template = Template(filename='template.html')
        lines = [line for p in article.findChildren('p') if (line := p.decode_contents())]

        return template.render(
            title_with_ruby=news['title_with_ruby'],
            top_priority_number=news['top_priority_number'],
            news_prearranged_time=news['news_prearranged_time'],
            news_id=news['news_id'],
            article=lines
        )

    @staticmethod
    def _write_file(filename, content):
        with open(filename, 'w+', encoding='utf-8') as handle:
            handle.writelines(content)


def main(args):  # pragma: no cover
    nhk = NHKNewsdl(args.days, args.path, args.date)
    nhk.download()


if __name__ == '__main__':  # pragma: no cover
    parser = argparse.ArgumentParser(prog="NHK News Web Easy Downloader")
    parser.add_argument('--path', '-p', action='store', default='nhknews_dump', help='Directory name to save news')
    parser.add_argument('--days', '-d', action='store', type=int, help='Number of days to download since today')
    parser.add_argument('--date', action='store', type=str, help='Date (YYYY-MM-DD format) to download news from')
    parser.add_argument('--version', '-V', action='version', version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    main(args)
