#!/usr/bin/env python3.11
"""Download news from http://www3.nhk.or.jp/news/easy/index.html"""

import os
import requests
import lxml.html
import lxml.etree


def get_news_list():
    """Download news list"""

    response = requests.get("http://www3.nhk.or.jp/news/easy/news-list.json")

    if response.ok:
        return sorted(response.json()[0].items())
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
    html_string.append('\t\t\t<li>Priority: ' + news['news_priority_number'] + '</li>\n')
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


def main():
    """Download all news and dictionary files to 'save_dir' folder"""

    # config
    save_dir = "nhknews_dump"
    os.makedirs(save_dir, exist_ok=True)

    news_list = get_news_list()
    if news_list:
        for date, news in news_list:
            print("Saving: " + date)
            os.makedirs(os.path.join(save_dir, date), exist_ok=True)
            for n in news:
                print("Saving:\t\tNews " + n['news_priority_number'], end='')
                file_html = os.path.join(save_dir, date, n['news_priority_number'] + '.html')
                try:
                    url = "http://www3.nhk.or.jp/news/easy/" + n['news_id'] + "/" + n['news_id'] + ".html"
                    parsed_html = prepare_html(lxml.html.parse(url).getroot().cssselect('#js-article-body p'), n)
                    with open(file_html, 'w+', encoding='utf-8', newline='\r\n') as handle:
                        handle.writelines(parsed_html)
                        print(" html ", end='')
                    response = requests.get("http://www3.nhk.or.jp/news/easy/" + n['news_id'] + "/" + n['news_id'] + ".out.dic")
                    response.encoding = 'utf-8'
                    if response.ok:
                        file_dic = os.path.join(save_dir, date, n['news_priority_number'] + '.dic.js')
                        with open(file_dic, 'w+', encoding='utf-8') as handle:
                            handle.write(response.text)
                            print("dic")
                except OSError as err:
                    print(" ERR ", end='\n')

    else:
        print("Error downloadig news!")


if __name__ == '__main__':
    main()
