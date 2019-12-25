日本語Wikipediaの分かち書き化
=======================================================================

jawiki.model は、python [gensim](https://radimrehurek.com/gensim/) の Word2Vec モデルを日本語Wikipediaで学習させたセーブファイルである。

サイズが約1GBとなるため、git上に保管できないため、作成手順のみ簡単に記載する。


# 作成手順

## 日本語Wikipediaアーカイブのダウンロード

```/etc/apt/apt.conf``` にproxyサイトを設定済みとする。

```
apt-get -y install mecab mecab-ipadic-utf8 git curl xz
curl https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2 -x solidproxy.exa-corp.co.jp:8080 -o jawiki-latest-pages-articles.xml.bz2
```

上記処理は、長時間かかるので帰宅直前などネットワークの空いた時間にバッチとして実行しておく。

## XMLをテキストへ変換

アーカイブはXML型式であるため、 ```ruby``` の ```wp2txt``` を使ってテキスト化する。

```
apt-get -y install ruby
gem install bandler wp2txt -r -p http://solidproxy.exa-corp.co.jp:8080/
wp2txt --input-file jawiki-latest-pages-articles.xml.bz2
cat jawiki-latest-pages-articles.xml-* > jawiki.txt
```

```rbenv`` 環境なら ```exec``` を付けて実行する。

## 分かち書き化

```
git config --global http.proxy http://solidproxy.exa-corp.co.jp:8080/
git config --global https.proxy http://solidproxy.exa-corp.co.jp:8080/
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd
echo `mecab-config --dicdir`"/mecab-ipadic-neologd"
echo `mecab-config --dicdir`"/mecab-ipadic-neologd" ←インストール先確認
mecab -d <mecab-ipadic-neologdインストール先フルパス> -Owakati jawiki.txt > jawiki_wakati.txt
```

## 文字コードや改行の調整

```
apt-get -y install file nkf
nkf -Lu jawiki.txt > jawiki_unix_utf8.txt ← UNIX改行、UTF-8型式
nkf -Ws jawiki.txt > jawiki_win_sjis.txt ←Windows改行、Shify_JIS型式
nkf -Lu jawiki_wakati.txt > jawiki_wakati_unix_utf8.txt ← UNIX改行、UTF-8型式
nkf -Ws jawiki_wakati.txt > jawiki_wakati_win_sjis.txt ←Windows改行、Shify_JIS型式
```

## genshim のインストール

python実行可能なコンソール上で以下のコマンドを実行する。

```
pip install gensim --proxy=http://solidproxy.exa-corp.co.jp:8080
```

## 学習およびセーブファイル保存

jupyter notebookやpython対話形式コンソールで以下を実行する。

```python
from gensim.models import word2vec
data = word2vec.Text8Corpus("jawiki_wakati_unix_utf8.txt") ←UNIX上で作業の場合
model = word2vec.Word2Vec(data, size=100)
model.save("jawiki.model")
```

```npy``` ファイルも一緒に保存しておくこと。

# ダウンロード

* [学習済みモデル tar.gz型式](http://www-end.exa-corp.co.jp/pukiwiki/file/AI/samples/jawiki_model.tar.gz)
