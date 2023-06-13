#!/usr/bin/env python3.11
"""Download news from https://www3.nhk.or.jp/news/easy/index.html"""
import argparse
import io
import os

import lxml.etree
import lxml.html
import requests
from mako.template import Template
from requests.exceptions import RequestException

__version__ = 1.6


class NHKNewsdl:
    NEWS_URL = "https://www3.nhk.or.jp/news/easy/{news_id}/{news_id}"
    NEWS_HTML_URL = f"{NEWS_URL}.html"
    NEWS_DICT_URL = f"{NEWS_URL}.out.dic"

    def __init__(self, days, save_path):
        self.days = days
        self.save_path = save_path

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
        limit = -self.days if self.days else None
        if response.ok:
            return sorted(response.json()[0].items())[limit:]
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

            parsed_html = self._prepare_html(
                lxml.html.parse(io.StringIO(response_html.text)).getroot().cssselect('#js-article-body p'), post)

            self._write_file(file_html, parsed_html)
            print(" html ", end='')
            self._write_file(file_dic, response_dict.text)
            print("dic")

        except RequestException as err:
            print(" ERR ", err, end='\n')

    @staticmethod
    def _prepare_html(article, news):
        template = Template(filename='template.html')
        lines = [line for p in article if
                 (line := lxml.etree.tostring(p, encoding='utf8').decode('utf8').strip()[3:-4])]

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


def main(args):
    nhk = NHKNewsdl(args.days, args.path)
    nhk.download()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="NHK News Web Easy Downloader")
    parser.add_argument('--path', '-p', action='store', default='nhknews_dump', help='Directory name to save news')
    parser.add_argument('--days', '-d', action='store', type=int, help='Number of days to download since today')
    parser.add_argument('--version', '-V', action='version', version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    main(args)
