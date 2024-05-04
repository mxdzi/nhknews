import datetime
import json
from unittest.mock import MagicMock, Mock, patch, mock_open

from nhknewsdownloader import NHKNewsdl


@patch('nhknewsdownloader.requests.get')
@patch('os.makedirs')
@patch('builtins.open', mock_open())
def test_download_post(mock_makedirs, mock_request, capsys):
    mock_response_list = Mock()
    mock_response_list.json.return_value = json.loads(data_json)

    mock_response_html = Mock()
    mock_response_html.text = data_html

    mock_request.side_effect = [mock_response_list, mock_response_html, Mock()]

    nhk = NHKNewsdl(1, 'test_dump')
    nhk.download()

    captured = capsys.readouterr()
    output = ("Saving: 2023-11-15\n"
              "Saving:\t\tNews 1 html dic\n")
    assert mock_makedirs.call_count == 2
    assert captured.out == output

@patch('nhknewsdownloader.requests.get')
@patch('os.makedirs')
@patch('builtins.open', mock_open())
def test_download_post_from_date(mock_makedirs, mock_request, capsys):
    mock_response_list = Mock()
    mock_response_list.json.return_value = json.loads(data_json)

    mock_response_html = Mock()
    mock_response_html.text = data_html

    mock_request.side_effect = [mock_response_list, mock_response_html, Mock()]

    nhk = NHKNewsdl(None, 'test_dump', '2022-02-22')
    nhk.download()

    captured = capsys.readouterr()
    output = ("Saving: 2022-02-22\n"
              "Saving:\t\tNews 1 html dic\n")
    assert mock_makedirs.call_count == 2
    assert captured.out == output


@patch('nhknewsdownloader.requests.get')
@patch('os.makedirs')
@patch('builtins.open', mock_open())
def test_download_news_list_fail(mock_makedirs, mock_request, capsys):
    mock_response_list = Mock()
    mock_response_list.ok = False

    mock_request.side_effect = [mock_response_list]

    nhk = NHKNewsdl(1, 'test_dump')
    nhk.download()

    captured = capsys.readouterr()
    output = "Error downloading news!\n"
    assert mock_makedirs.call_count == 0
    assert captured.out == output


@patch('nhknewsdownloader.requests.get')
@patch('os.makedirs')
@patch('builtins.open', mock_open())
def test_download_news_post_fail(mock_makedirs, mock_request, capsys):
    mock_response_list = Mock()
    mock_response_list.json.return_value = json.loads(data_json)

    mock_response_html = Mock()
    mock_response_html.text = data_html
    from requests.exceptions import HTTPError
    mock_request.side_effect = [mock_response_list, mock_response_html, HTTPError]

    nhk = NHKNewsdl(1, 'test_dump')
    nhk.download()

    captured = capsys.readouterr()
    output = "Saving: 2023-11-15\nSaving:\t\tNews 1 ERR  \n"
    assert mock_makedirs.call_count == 2
    assert captured.out == output


data_json = """
[
  {
    "2023-11-15": [
      {
        "top_priority_number": 1,
        "news_prearranged_time": "2023-11-15 16:20:00",
        "news_id": "k10014257381000",
        "title_with_ruby": "\u30a6\u30a7\u30d6\u30b5\u30a4\u30c8\u3067\u30db\u30c6\u30eb\u306e<ruby>\u4e88\u7d04<rt>\u3088\u3084\u304f</rt></ruby>\u3000\u30ab\u30fc\u30c9\u306e<ruby>\u60c5\u5831<rt>\u3058\u3087\u3046\u307b\u3046</rt></ruby>\u3092<ruby>\u76d7<rt>\u306c\u3059</rt></ruby>\u307e\u308c\u308b<ruby>\u88ab\u5bb3<rt>\u3072\u304c\u3044</rt></ruby>"
      }
    ],
    "2022-02-22": [
      {
        "top_priority_number": 1,
        "news_prearranged_time": "2022-02-22 12:00:00",
        "news_id": "k10099999999999",
        "title_with_ruby": "Title with Ruby"
      }
    ]
  }
]
"""

data_html = """<!DOCTYPE HTML>
<head>
<meta charset="utf-8">
<title>ウェブサイトでホテルの予約　カードの情報を盗まれる被害|NEWS WEB EASY</title>
</head>
<body id="news20231115_k10014257381000">
<div id="wrapper">
  <div id="content">
    <div class="easy-wrapper" id="easy-wrapper">
      <div class="l-container">
        <main class="l-main">
          <article class="article-main">
            <div class="article-main__body article-body" id="js-article-body">
                <p><span class="colorB">「</span><span class="colorF">ブッキング・ドットコム</span><span class="colorB">」</span><span class="colorB">は</span><span class="color4">ホテル</span><span class="color4">など</span><span class="colorB">の</span><span class="color3"><ruby>予約<rt>よやく</rt></ruby></span><span class="colorB">をする</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-002044"><span class="color0"><span class="under">ウェブサイト</span></span></a><span class="colorB">です</span><span class="colorB">。</span><span class="colorC"><ruby>観光庁<rt>かんこうちょう</rt></ruby></span><span class="colorB">によると</span><span class="colorB">、</span><span class="colorB">この</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-002044"><span class="color0"><span class="under">ウェブサイト</span></span></a><span class="colorB">で</span><span class="color3"><ruby>予約<rt>よやく</rt></ruby></span><span class="colorB">を</span><span class="colorB">した</span><span class="colorB"><ruby>人<rt>ひと</rt></ruby>が</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-007884"><span class="color0"><span class="under">クレジットカード</span></span></a><span class="colorB">の</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-013566"><span class="color2"><ruby><span class="under">情報</span><rt>じょうほう</rt></ruby></span></a><span class="colorB">を</span><span class="color3"><ruby>盗<rt>ぬす</rt></ruby>ま</span><span class="colorB">れる</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-023723"><span class="color2"><ruby><span class="under">被害</span><rt>ひがい</rt></ruby></span></a><span class="colorB">が</span><span class="color4">あり</span><span class="colorB">ました</span><span class="colorB">。</span></p>
                <p><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-002044"><span class="color0"><span class="under">ウェブサイト</span></span></a><span class="colorB">の</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-011745"><span class="color1"><span class="under">システム</span></span></a><span class="colorB">に</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-025004"><span class="color2"><ruby><span class="under">不正</span><rt>ふせい</rt></ruby></span></a><span class="colorB">に</span><span class="color4"><ruby>入<rt>はい</rt></ruby>っ</span><span class="colorB">た</span><span class="color4"><ruby>誰<rt>だれ</rt></ruby></span><span class="colorB">か</span><span class="colorB">が</span><span class="colorB">、</span><span class="color3"><ruby>予約<rt>よやく</rt></ruby></span><span class="colorB">を</span><span class="color4">し</span><span class="colorB">た</span><span class="color4"><ruby>人<rt>ひと</rt></ruby></span><span class="colorB">に</span><span class="colorB">「</span><span class="color3"><ruby>泊<rt>と</rt></ruby>まる</span><span class="color4"><ruby>前<rt>まえ</rt></ruby></span><span class="colorB">に</span><span class="color4">お<ruby>金<rt>かね</rt></ruby></span><span class="colorB">を</span><span class="color3"><ruby>払<rt>はら</rt></ruby>っ</span><span class="colorB">て</span><span class="color3">ください</span><span class="colorB">」</span><span class="color4">など</span><span class="colorB">の</span><span class="color3">うそ</span><span class="colorB">の</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-028409"><span class="color1"><span class="under">メッセージ</span></span></a><span class="colorB">を</span><span class="color3"><ruby>送<rt>おく</rt></ruby>っ</span><span class="colorB">て</span><span class="color4">い</span><span class="colorB">ます</span><span class="colorB">。</span><span class="color4">そして</span><span class="colorB">、</span><span class="color3">うそ</span><span class="colorB">の</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-002044"><span class="color0"><span class="under">ウェブサイト</span></span></a><span class="colorB">で</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-007884"><span class="color0"><span class="under">クレジットカード</span></span></a><span class="colorB">の</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-013566"><span class="color2"><ruby><span class="under">情報</span><rt>じょうほう</rt></ruby></span></a><span class="colorB">を</span><span class="color4"><ruby>聞<rt>き</rt></ruby>い</span><span class="colorB">て</span><span class="colorB">、</span><span class="color3"><ruby>盗<rt>ぬす</rt></ruby>ん</span><span class="colorB">で</span><span class="color3">い</span><span class="colorB">ます</span><span class="colorB">。</span></p>
                <p><span class="colorL"><ruby>日本<rt>にっぽん</rt></ruby></span><span class="color4">だけ</span><span class="colorB">ではなくて</span><span class="colorB">、</span><span class="color3"><ruby>世界<rt>せかい</rt></ruby></span><span class="colorB">で</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-023723"><span class="color2"><ruby><span class="under">被害</span><rt>ひがい</rt></ruby></span></a><span class="colorB">が</span><span class="color4">あっ</span><span class="colorB">た</span><span class="color4">こと</span><span class="colorB">が</span><span class="color4">わかっ</span><span class="colorB">て</span><span class="color4">い</span><span class="colorB">ます</span><span class="colorB">。</span></p>
                <p><span class="colorC"><ruby>観光庁<rt>かんこうちょう</rt></ruby></span><span class="colorB">は</span><span class="colorB">「</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-002044"><span class="color0"><span class="under">ウェブサイト</span></span></a><span class="colorB">の</span><span class="color4"><ruby>会社<rt>かいしゃ</rt></ruby></span><span class="colorB">は</span><span class="colorB">、</span><span class="color3"><ruby>予約<rt>よやく</rt></ruby></span><span class="colorB">をする</span><span class="color4"><ruby>人<rt>ひと</rt></ruby></span><span class="colorB">に</span><span class="color3"><ruby>気<rt>き</rt></ruby>をつける</span><span class="colorB">よう</span><span class="colorB">に</span><span class="color4"><ruby>言<rt>い</rt></ruby>っ</span><span class="colorB">て</span><span class="color3">ください</span><span class="colorB">」</span><span class="colorB">と</span><span class="color4"><ruby>言<rt>い</rt></ruby>い</span><span class="colorB">ました</span><span class="colorB">。</span></p>
                <p><span class="color4"><ruby>会社<rt>かいしゃ</rt></ruby></span><span class="colorB">は</span><span class="colorB">「</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-028409"><span class="color1"><span class="under">メッセージ</span></span></a><span class="colorB">で</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-007884"><span class="color0"><span class="under">クレジットカード</span></span></a><span class="colorB">の</span><a href="javascript:void(0)" class="dicWin" id="RSHOK-K-013566"><span class="color2"><ruby><span class="under">情報</span><rt>じょうほう</rt></ruby></span></a><span class="colorB">を</span><span class="color4"><ruby>聞<rt>き</rt></ruby>く</span><span class="color4">こと</span><span class="colorB">は</span><span class="color4">あり</span><span class="colorB">ませ</span><span class="colorB">ん</span><span class="colorB">」</span><span class="colorB">と</span><span class="color4"><ruby>言<rt>い</rt></ruby>っ</span><span class="colorB">て</span><span class="color4">い</span><span class="colorB">ます</span><span class="colorB">。</span></p>
            </div>
          </article>
        </main>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""
