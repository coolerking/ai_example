# jawiki.model ファイルの作り方

jawiki.model ファイルのサイズが約100MBとなるため、作成手順の記述に留める。

## jawiki_wakati.txt の作成

[Qiita記事]:http://qiita.com/tsuruchan/items/7d3af5c5e9182230db4e に記載された手順で日本語Wikipediaデータをjawiki_wakati.txt を作成する。

## jawiki.model ファイルの作成

以下の手順でgensimパッケージを使ってjawiki.modelファイルを作成する。

    from gensim.models import word2vec
    data = word2vec.Text8Corpus("jawiki_wakati.txt")
    model = word2vec.Word2Vec(data, size=100)
    model.save("jawiki.model")

# jawiki.model ダウンロード

既に学習済みのモデルをダウンロード可能である。
以下のリンクよりダウンロードし、本ディレクトリへ格納すること。

* [学習済みモデル tar.gz型式](http://www-end.exa-corp.co.jp/pukiwiki/file/AI/samples/jawiki_model.tar.gz)
