# -*- coding: utf-8 -*-
"""聖書コーパスユーティリティ

本モジュールは聖書コーパス(bible.py)のユーティリティを集約したものです。

(C) Tasuku Hori, exa Corporation Japan, 2017. all rights reserved.
"""

__author__ = 'Tasuku Hori'

from collections import Counter
import csv
import random
import numpy as np


class TranslatorCorpus():
    """機械翻訳コーパスをあらわすクラス
    """

    def __init__(self, csv_path='testament_utf8_unix.csv', array=None, x_seq_len=200, y_seq_len=100):
        """testament.py のアウトプットであるCSVファイルを読み込み
        もしくはBible.corpusを使って
        日英翻訳データセットをインスタンス変数へ格納する。
        csv_path: CSVファイルのパス文字列(デフォルト:'testament_utf8_unix.csv')
        array: Bibleコーパス文字列(デフォルト: None)
        x_seq_len: 第1言語特徴量ベクトル長(デフォルト: 200)
        y_seq_len: 第2言語特徴量ベクトル長(デフォルト: 100)
        """

        # Bible.corpus 指定がない場合
        if array == None:
            # CSVファイルから１行１要素配列、全単語配列を取得
            x, y, x_words, y_words = TranslatorCorpus.read_csv(csv_path)
        # Bible.corpus 指定がある場合
        else:
            # 配列から切り出す
            x, y, x_words, y_words = TranslatorCorpus.read_array(array)

        # ID配列、正引き辞書の作成
        x_int, x_vocab, x_vocab_to_int = TranslatorCorpus.words_to_ids(x, x_words)
        y_int, y_vocab, y_vocab_to_int = TranslatorCorpus.words_to_ids(y, y_words)


        # 第１言語側に空行がある場合、該当業のみ削除する

        # 英語・日本語配列から1行データ(idの配列)を取り出し、単語数を抽出 len(x), len(y)
        # 文章のIDと単語数の辞書化
        x_lens = Counter([len(x) for x in x_int])
        y_lens = Counter([len(y) for y in y_int])

        # ID化された配列から単語数が0でない行を1行づつ取り出し行番号-1の値を配列化する
        x_non_zero_idx = [ii for ii, x in enumerate(x_int) if len(x) != 0]

        # 単語数0でない行数
        #print("ENG non-zero length lines: ", len(x_non_zero_idx))

        # x_int,y_int をx側単語数0でないものだけにする
        x_int = [ x_int[ii] for ii in x_non_zero_idx]
        y_int = [ y_int[ii] for ii in x_non_zero_idx] # x_non_zero_idsでOK

        # 英語・日本語配列から1行データ(idの配列)を取り出し、単語数を抽出 len(x), len(y)
        # 文章のIDと単語数の辞書化
        x_lens = Counter([len(x) for x in x_int])
        y_lens = Counter([len(y) for y in y_int])

        ##第2言語側に空行がある場合、該当業のみ削除する

        # ID化された配列から単語数が0でない行を1行づつ取り出し行番号-1の値を配列化する
        y_non_zero_idx = [ii for ii, y in enumerate(y_int) if len(y) != 0]

        # 単語数0でない行数
        #print("JPN non-zero length lines: ", len(y_non_zero_idx))

        # y_int,y_int をy側単語数0でないものだけにする
        x_int = [ x_int[ii] for ii in y_non_zero_idx] # y_non_zero_idsでOK
        y_int = [ y_int[ii] for ii in y_non_zero_idx]

        # 英語・日本語配列から1行データ(idの配列)を取り出し、単語数を抽出 len(x), len(y)
        # 文章のIDと単語数の辞書化
        x_lens = Counter([len(x) for x in x_int])
        y_lens = Counter([len(y) for y in y_int])

        #

        # レビューの長さを100, 200に制限する
        x_seq_len = 100
        y_seq_len = 200

        # 特徴ベクトルをつくる
        # 型式が(レビュー行数, レビュー上限長)で要素がintのnumpy配列を0で初期化
        x_features = np.zeros((len(x_int), x_seq_len), dtype=int)
        y_features = np.zeros((len(y_int), y_seq_len), dtype=int)

        # 英語

        # カウンタ(i)とレビュー1行(row)を取り出し
        for i, row in enumerate(x_int):
            # 前方が0を埋めて行を構成するid値で埋めるが
            # 最大長(x_seq_len)を超えないように切っている
            x_features[i, -len(row):] = np.array(row)[:x_seq_len]

        # 日本語

        # カウンタ(i)とレビュー1行(row)を取り出し
        for i, row in enumerate(y_int):
            # 前方が0を埋めて行を構成するid値で埋めるが
            # 最大長(y_seq_len)を超えないように切っている
            y_features[i, -len(row):] = np.array(row)[:y_seq_len]

        # インスタンス変数化
        self.x = x
        self.y = y
        self.x_words = x_words
        self.y_words = y_words

        # 特徴量行列から、用途別に切り出す
        self.train_x, self.val_x, self.test_x = TranslatorCorpus.split_corpus(x_features)
        self.train_y, self.val_y, self.test_y = TranslatorCorpus.split_corpus(y_features)
        # 正引き辞書
        self.x_vocab_to_int = x_vocab_to_int
        self.y_vocab_to_int = y_vocab_to_int
        # 逆引き辞書
        self.x_int_to_vocab = {v:k for k, v in x_vocab_to_int.items()}
        self.y_int_to_vocab = {v:k for k, v in y_vocab_to_int.items()}
        # 語彙
        self.x_vocab = x_vocab
        self.y_vocab = y_vocab

    def save_vocab(self):
        """ インスタンス変数から語彙ファイルを書き出す。
        """
        self.write_x_vocab_to_file()
        self.write_y_vocab_to_file()

    def write_x_vocab_to_file(self, x_vocab_path='x_vocab.txt'):
        """ 第1言語の語彙をファイル(x_vocab_path)へ書き出す。
        x_vocab_path: 第1言語の語彙ファイル(デフォルト:'x_vocab.txt')
        """
        self._write_vocab_to_file(x_vocab_path, self.x_vocab)

    def write_y_vocab_to_file(self, y_vocab_path='y_vocab.txt'):
        """ 第2言語の語彙をファイル(y_vocab_path)へ書き出す。
        y_vocab_path: 第2言語の語彙ファイル(デフォルト:'y_vocab.txt')
        """
        self._write_vocab_to_file(y_vocab_path, self.y_vocab)

    def _write_vocab_to_file(self, vocab_path, vocab):
        """ 引数vocab_pathで渡されたパス先へ語彙vocabを保存する。
        ファイルは１語１行とする。
        """
        with open(vocab_path, 'w', encoding='UTF-8') as f:
            for word in vocab:
                f.write(word + "\n")

    def x_feature_to_sentence(self, x_feature):
        """ １件分の特徴量ベクトル(x_feature)を第1言語の文章に変換する。
        """
        return TranslatorCorpus.feature_to_sentence(x_feature, self.x_int_to_vocab)

    def y_feature_to_sentence(self, y_feature):
        """ １件分の特徴量ベクトル(y_feature)を第2言語の文章に変換する。
        """
        return TranslatorCorpus.feature_to_sentence(x_feature, self.y_int_to_vocab, separator='')

    def print_statistics(self, save=False):
        """ コーパス統計情報を表示する。
        save: 語彙ファイルを書き出し、インスタンス変数の内容と比較するか(デフォルト:False)
        """
        print("X-Lang total available lines: ", len(self.x))
        print("Y-Lang total available lines: ", len(self.y))
        print("*-" * 40)
        print("X-Lang total words: ", len(self.x_words))
        print("X-Lang total vocab: ", len(self.x_vocab))
        print()
        print("X-Lang training set   \t{}".format(self.train_x.shape))
        print("X-Lang validation set \t{}".format(self.val_x.shape))
        print("X-Lang test set       \t{}".format(self.test_x.shape))
        print("- " * 40)
        print("Y-Lang total words: ", len(self.y_words))
        print("Y-Lang total vocab: ", len(self.y_vocab))
        print()
        print("Y-Lang training set   \t{}".format(self.train_y.shape))
        print("Y-Lang validation set \t{}".format(self.val_y.shape))
        print("Y-Lang test set       \t{}".format(self.test_y.shape))
        if save == True:
            self.save_vocab()
            x_vocab, x_int_to_vocab, x_vocab_to_int = TranslatorCorpus.read_x_vocab_file()
            y_vocab, y_int_to_vocab, y_vocab_to_int = TranslatorCorpus.read_y_vocab_file()
            print("*-" * 40)
            print("X-Lang vocab file assertion:", x_vocab[0] == self.x_vocab[0])
            print("Y-Lang vocab file assertion:", y_vocab[0] == self.y_vocab[0])

    @staticmethod
    def read_csv(csv_path):
        """ CSVファイルを読み込み、
        最初の言語の1行1要素(x)、２番めの言語の１行１要素(y)、
        最初の言語の全単語重複有り(x_words)、２番めの言語の全単語重複有り(y_words)を
        返却する。
        """

        x = [] # 英語配列　1行1要素
        y = [] # 日本語配列 1行1要素
        x_words = [] # 英語全単語　重複有り
        y_words = [] # 日本語全単語　重複有り
        with open(csv_path, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            for row in reader:
                x.append(row[0].split())
                x_words.extend(row[0].split())
                y.append(row[1].split())
                y_words.extend(row[1].split())
        return x, y, x_word, y_word

    @staticmethod
    def read_array(array):
        """ 配列型式([["第１言語の文1", "第2言語の文2"],
        ["第１言語の文2", "第2言語の文2"],.. ])から、
        最初の言語の1行1要素(x)、２番めの言語の１行１要素(y)、
        最初の言語の全単語重複有り(x_words)、２番めの言語の全単語重複有り(y_words)を
        返却する。
        """

        x = [] # 英語配列　1行1要素
        y = [] # 日本語配列 1行1要素
        x_words = [] # 英語全単語　重複有り
        y_words = [] # 日本語全単語　重複有り
        for row in array:
            x.append(row[0].split())
            x_words.extend(row[0].split())
            #x_lines.append(row[0].split())
            y.append(row[1].split())
            y_words.extend(row[1].split())
            #y_lines.append(row[1].split())
        return x, y, x_words, y_words

    @staticmethod
    def words_to_ids(all_lines, all_words):
        """行単位にID化した配列(ids)、高頻度順の単語集(vocab)、
        IDから単語への正引き辞書(int_to_vocab)に変換
        all_lines: 分かち書き済みの１行１要素配列
        all_words: 分かち済み単語１語１要素配列
        """
        # 単語と頻度の辞書へ
        counts = Counter(all_words)

        # 頻度の降順に並べ直す
        vocab = sorted(counts, key=counts.get, reverse=True)

        # 辞書の先頭からIDを振り、単語とIDの辞書を作成
        vocab_to_int = {word:i for i,word in enumerate(vocab, 1)}

        # ID配列の初期化
        ids = []
        #
        for line in all_lines:
            # 1行を空白で切り出して単語にしてそのidに変換し配列化する
            ids.append([vocab_to_int[word] for word in line])

        # 行単位にID化した配列、正引き辞書を返却
        return ids, vocab, vocab_to_int


    @staticmethod
    def split_corpus(features, train_rate=0.8, test_rate=0.1, val_rate=0.1):
        """データ(feature)をトレーニング用(train)、テスト用(test)、検証用(val)に分割
        train_rate: トレーニング用データの分割比率(デフォルト0.8)
        test_rate: テスト用データの分割比率(デフォルト0.1)
        val_rate: 検証用データの分割比率(デフォルト0.1)
        """
        # 総件数
        total = len(features)

        # 比率の分母
        rate_total = float(train_rate) + float(test_rate) + float(val_rate)
        # トレーニングデータ最後の位置
        idx_train = int( (float(train_rate) / rate_total) * total)
        # トレーニング+テストデータ最後の位置
        idx_test =int( (float(test_rate) / rate_total) * total) + idx_train

        # リストを比率で分割
        return features[:idx_train], features[idx_train:idx_test], features[idx_test:]

    @staticmethod
    def feature_to_sentence(feature, int_to_vocab, separator=' '):
        """ 特徴量ベクトル(features)を逆引き辞書(int_to_vocab)を使って
        文章に変換する。その際のセパレータ(separator)を指定することが可能。
        feature: 1件分の特徴量ベクトル(1次元リスト)
        int_to_vocab: ID→単語 用辞書
        separator: セパレータ文字列(デフォルト:' ')
        """
        return separator.join([int_to_vocab[id] for id in feature if 0 < id])

    @staticmethod
    def get_reverse_dict(dictionary):
        """ 引数(dictionary)で渡された辞書のキーと値を反転させた辞書を返却する。
        """
        return {v:k for k, v in dictionary.items()}


    @staticmethod
    def read_x_vocab_file(x_vocab_path='x_vocab.txt'):
        """ 第1言語の語彙ファイル(x_vocab_path)を読み込み
        語彙リスト(x_vocab)、正引き辞書(x_int_to_vocab)、
        逆引き辞書(x_vocab_to_int) を復元する。
        x_vocab_path: 第1言語の語彙ファイル(デフォルト:'x_vocab.txt')
        """
        x_vocab, x_int_to_vocab, x_vocab_to_int = TranslatorCorpus.read_vocab_file(x_vocab_path)
        return x_vocab, x_int_to_vocab, x_vocab_to_int

    @staticmethod
    def read_y_vocab_file(y_vocab_path='y_vocab.txt'):
        """ 第2言語の語彙ファイル(y_vocab_path)を読み込み
        語彙リスト(y_vocab)、正引き辞書(y_int_to_vocab)、
        逆引き辞書(y_vocab_to_int) を復元する。
        y_vocab_path: 第2言語の語彙ファイル(デフォルト:'y_vocab.txt')
        """
        y_vocab, y_int_to_vocab, y_vocab_to_int = TranslatorCorpus.read_vocab_file(y_vocab_path)
        return y_vocab, y_int_to_vocab, y_vocab_to_int

    @staticmethod
    def read_vocab_file(vocab_path):
        """ 語彙ファイルを読み込み語彙リスト(vocab)、
        正引き辞書(int_to_vocab)、逆引き辞書(vocab_to_int) を復元する。
        """
        idx = 0
        vocab = []
        vocab_to_int = {}
        int_to_vocab = {}
        with open(vocab_path, 'r', encoding='UTF-8') as f:
            for row in f:
                idx += 1
                word = row.split()[0]
                vocab_to_int[word] = idx
                int_to_vocab[idx] = word
                vocab.append(word)
        return vocab, int_to_vocab, vocab_to_int

def main():
    """ ローカルの聖書コーパスデータをもとにBibleを復元し、
    本クラスへ渡して、各用途ごとのコーパス情報を表示する
    """
    from bible import Bible
    bible = Bible()
    print()
    print("*-" * 40)
    print("Copus statistics")
    print("*-" * 40)
    print("Total lines:                  ", len(bible.corpus))

    c = TranslatorCorpus(array=bible.corpus)
    c.print_statistics(save=True)

if __name__ == '__main__':
    main()
