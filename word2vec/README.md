# アプリケーションの起動方法

## 事前準備

### 環境
Python3が導入されていることとする。

gensimが導入されていない場合は、pipコマンドを使ってインストールしておくこと：
    pip install gensim

ポート番号3000を使用するので、該当ポートを使用するアプリケーションを停止させておくこと。

### 学習済みモデルファイル

本アプリケーションを起動するには ml/store/jawiki.model が必要となる。
jawiki.model 作成方法については ml/store/HowToCreate_jawiki.model.md を参照のこと。

## 起動

以下のコマンドを実行して、起動する。
    python run_application

## 使い方

入力フィールドに日本語の単語を記入し、実行ボタンを押すと、画面下部に類似語が表示される。

## 停止方法

Ctrl+C を押し、run_application.py を停止する。
