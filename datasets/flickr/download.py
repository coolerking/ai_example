# -*- coding: utf-8 -*-
from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys

# APIキー情報
#
# Flickrサイトにサインインして
# APIキー、秘密キーをそれぞれ取得し、各変数を書き換える
key = "08db85f915d3e749410e5fxxxxxxxxxx"
secret = "4165f2xxxxxxxxxx"
# 待機秒数
wait_time = 1

# 検索キーワード
#
# 検索対象のキーワードリスト
# カレントディレクトリ上に同名のフォルダが作成される。
keywords = ["monkey", "boar", "crow"]
#keywords = ["boar", "crow"]



for keyword in keywords:
    if not os.path.exists('./' + keyword):
        os.makedirs('./' + keyword)
    # API送信
    flickr = FlickrAPI(key, secret, format='parsed-json')
    result = flickr.photos.search(
        text = keyword,
        per_page = 400,
        media = 'photons',
        sort = 'relevance',
        safe_search = 1,
        extras = 'url_q, licence'
    )
    photos = result['photos']
    for i, photo in enumerate(photos['photo']):
        url_q = photo['url_q']
        filepath = './' + keyword + '/' + photo['id'] + '.jpg'
        if os.path.exists(filepath):
            continue
        urlretrieve(url_q, filepath)
        time.sleep(wait_time)
    print(keyword + " Done.")

print("Done.")
