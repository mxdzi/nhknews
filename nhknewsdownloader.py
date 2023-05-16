#!/usr/bin/env python3.11
"""Download news from http://www3.nhk.or.jp/news/easy/index.html"""
import argparse
import os
import requests
import lxml.html
import lxml.etree

__version__ = 1.3

# config
NEWS_URL = "http://www3.nhk.or.jp/news/easy/{news_id}/{news_id}"
NEWS_HTML_URL = f"{NEWS_URL}.html"
NEWS_DICT_URL = f"{NEWS_URL}.out.dic"


def get_news_list(days):
    """Download news list"""

    response = requests.get("http://www3.nhk.or.jp/news/easy/news-list.json")

    if response.ok:
        return sorted(response.json()[0].items())[-days if days else None:]
    else:
        return None


def prepare_html(article, news):
    """Create news HTML template"""

    html_string = []

    html_string.append('<!DOCTYPE html>\n<html>\n\t<head>\n')
    html_string.append('\t\t<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n')
    html_string.append('\t\t<title>' + news['title_with_ruby'] + '</title>\n')
    html_string.append('\t</head>\n\t<body>\n')
    html_string.append('\t\t<ul>\n')
    html_string.append('\t\t\t<li>Title: ' + news['title_with_ruby'] + '</li>\n')
    html_string.append('\t\t\t<li>Priority: ' + str(news['top_priority_number']) + '</li>\n')
    html_string.append('\t\t\t<li>Date: ' + news['news_prearranged_time'] + '</li>\n')
    html_string.append('\t\t\t<li>Id: ' + news['news_id'] + '</li>\n')
    html_string.append('\t\t</ul>\n')
    html_string.append('\t\t<ol>\n')

    for p in article:
        if len(lxml.etree.tostring(p, encoding='utf8').decode('utf8').strip()[3:-4]) > 0:
            html_string.append('\t\t\t<li>' + lxml.etree.tostring(p, encoding='utf8').decode('utf8').strip()[3:-4] + '</li>\n')

    html_string.append('\t\t</ol>\n')
    html_string.append('\t</body>\n</html>')
    return html_string


def main(days, save_path):
    """Download all news and dictionary files to 'SAVE_DIR' folder"""

    os.makedirs(save_path, exist_ok=True)

    news_list = get_news_list(days)
    if news_list:
        for date, news in news_list:
            print("Saving: " + date)
            os.makedirs(os.path.join(save_path, date), exist_ok=True)
            for n in news:
                print("Saving:\t\tNews " + str(n['top_priority_number']), end='')
                try:
                    url_news = NEWS_HTML_URL.format(news_id=n['news_id'])
                    url_dict = NEWS_DICT_URL.format(news_id=n['news_id'])

                    file_name = os.path.join(save_path, date, str(n['top_priority_number']))
                    file_html = file_name + '.html'
                    file_dic = file_name + '.dic.js'

                    parsed_html = prepare_html(lxml.html.parse(url_news).getroot().cssselect('#js-article-body p'), n)
                    write_file(file_html, parsed_html)
                    print(" html ", end='')

                    response = requests.get(url_dict)
                    response.encoding = 'utf-8'
                    if response.ok:
                        write_file(file_dic, response.text)
                        print("dic")

                except OSError as err:
                    print(" ERR ", end='\n')
    else:
        print("Error downloading news!")


def write_file(filename, content):
    with open(filename, 'w+', encoding='utf-8') as handle:
        handle.writelines(content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="NHK News Web Easy Downloader")
    parser.add_argument('--path', '-p', action='store', default='nhknews_dump', help='Directory name to save news')
    parser.add_argument('--days', '-d', action='store', type=int, help='Number of days to download since today')
    parser.add_argument('--version', '-V', action='version', version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    main(args.days, args.path)
