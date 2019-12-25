# Flickr をキーワード検索し、対象の画像を400件づつ取得するサンプルコード

FlickrAPIを使ってインターネットサービスflickrに掲載されている画像データをコーパスとしたい場合に使用する。

## 前提
- flickr(yahoo.com) アカウント
- flickr API キー、秘密キー
- python 3.5.x
 - flickrapi
- Proxy環境の場合はHTTP_PROXY,HTTPS_PROXY設定

## 実行

1. download.py 上のFlickr APIキー、秘密キー、キーワードを書き換える
2. 以下のコマンドを実行する

```
python download.py
```

## ライセンス

- Python3.5.x: Pythonライセンス
- FlickrAPI: Pythonライセンス
