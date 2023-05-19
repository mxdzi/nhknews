#!/usr/bin/env python3.11
"""Download news from http://www3.nhk.or.jp/news/easy/index.html"""
import argparse
import os
import requests
import lxml.html
import lxml.etree
from mako.template import Template

__version__ = 1.5


class NHKNewsdl:
    NEWS_URL = "http://www3.nhk.or.jp/news/easy/{news_id}/{news_id}"
    NEWS_HTML_URL = f"{NEWS_URL}.html"
    NEWS_DICT_URL = f"{NEWS_URL}.out.dic"

    def __init__(self, days, save_path):
        self.days = days
        self.save_path = save_path

    def download(self):
        os.makedirs(self.save_path, exist_ok=True)

        news_list = self._get_news_list()
        if news_list:
            for date, news in news_list:
                print("Saving: " + date)
                os.makedirs(os.path.join(self.save_path, date), exist_ok=True)
                for n in news:
                    print("Saving:\t\tNews " + str(n['top_priority_number']), end='')
                    try:
                        url_news = self.NEWS_HTML_URL.format(news_id=n['news_id'])
                        url_dict = self.NEWS_DICT_URL.format(news_id=n['news_id'])

                        file_name = os.path.join(self.save_path, date, str(n['top_priority_number']))
                        file_html = file_name + '.html'
                        file_dic = file_name + '.dic.js'

                        parsed_html = self._prepare_html(
                            lxml.html.parse(url_news).getroot().cssselect('#js-article-body p'), n)
                        self._write_file(file_html, parsed_html)
                        print(" html ", end='')

                        response = requests.get(url_dict)
                        response.encoding = 'utf-8'
                        if response.ok:
                            self._write_file(file_dic, response.text)
                            print("dic")

                    except OSError as err:
                        print(" ERR ", end='\n')
        else:
            print("Error downloading news!")

    def _get_news_list(self):
        response = requests.get("http://www3.nhk.or.jp/news/easy/news-list.json")
        if response.ok:
            return sorted(response.json()[0].items())[-self.days if self.days else None:]
        else:
            return None

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
