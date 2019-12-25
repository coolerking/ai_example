# アプリケーションの起動方法

## 事前準備

### 環境
Python3が導入されていることとする。

janome が導入されていない場合は、pipコマンドを使ってインストールしておくこと：
    pip install janome

ポート番号3000を使用するので、該当ポートを使用するアプリケーションを停止させておくこと。

> 本アプリは、事前学習済みのモデルファイルなどの準備は不要。

## 起動

以下のコマンドを実行して、起動する。
    python run_application.py

## 使い方

入力フィールドに日本語の文章を記入し、実行ボタンを押すと、画面下部に分かち書き済みの文章として表示される。

## 停止方法

Ctrl+C を押し、run_application.py を停止する。

# Dockerコンテナとしての起動方法

```docker``` コマンドが使用可能な状態で、以下のコマンドを実行する。


```bash
$ git clone http://pandagit.exa-corp.co.jp/git/89004/ai_samples.git
$ cd ai_sample/wakati
$ sudo docker build .
  → 完成したイメージIDをメモしておく

$ sudo docker run -d -p 3333:3000 --name=wakati イメージID先頭3文字
  → http://ホスト側IPアドレス:3333/ をブラウザで開く
```

```-p 3333:3000``` は、ポート番号3000番でコンテナ側がlistenしている状態で、ホスト側ポート番号を3333で使いたい場合に指定する。

動作確認は、 ```sudo docker ps``` で確認できる。また、標準出力のログは ```sudo docker logs wakati``` で確認可能である。
