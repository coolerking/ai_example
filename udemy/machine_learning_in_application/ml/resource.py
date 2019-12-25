# coding: -*- utf-8 -*-
import os
import json
from datetime import datetime
import numpy as np
from chainer import serializers
from ml.data_processor import DataProcessor

# Resource クラス
#
# モデルパラメータのファイルへの保存、復元、
# MNISTトレーニングデータファイルへの読み書き、そして
# Chainerモデルクラスの保存、復元を管理するリソース操作クラス
# MNIST/Chainer実装になっているので、該当箇所を書き換えれば
# ほかの機械学習でも使える
class Resource():

    # 入力、出力データサイズ定義
    # MNIST以外で使用したい場合は書き換える

    # 入力サイズ：8ピクセル×8ピクセル×単色(1)の全要素数
    INPUT_SIZE = 64  # 8 x 8 image size
    # 出力サイズ：0から9までの数字の分類数
    OUTPUT_SIZE = 10  # 10 classification

    # コンストラクタ
    # 引数 root: パス文字列（指定なし→""）
    # →テスト時に作成される各種ファイルの振り出しを変えたいために存在する
    #
    # self はJavaのthis
    # コンストラクタ引数rootが指定されなかった場合は、空文字（≠空）を格納
    def __init__(self, root=""):
        # __file__ 実行中のスクリプトファイルを表す
        # コンストラクタ引数rootが空の場合
        # resource.pyのあるディレクトリ + "./store" を、
        # そうでない場合はコンストラクタ引数をそのまま、
        # インスタンス変数rootへ格納
        self.root = root if root else os.path.join(os.path.dirname(__file__), "./store")
        # インスタンス変数model_pathに
        # <resource.pyのあるディレクトリ>/store/model もしくは
        # <コンストラクタ引数rootの指すディレクトリ>/model を格納
        self.model_path = os.path.join(self.root, "./model")
        # インスタンス変数 param_file に
        # <resource.pyのあるディレクトリ>/store/params.json もしくは
        # <コンストラクタ引数rootの指すディレクトリ>/params.jeson を格納
        self.param_file = os.path.join(self.root, "./params.json")

    # 正規化パラメータを保存
    # 引数 means:
    # 引数 stds:
    # 戻り値なし
    #
    # 引数で与えられたデータを1行文字列化してparam_fileへ書き込む
    def save_normalization_params(self, means, stds):
        # 引数lsを持つto_list関数を定義
        # ls値がtupleかlistのどちらかであればls値そのままを、
        # そうでなければls値をリスト化して返却する
        to_list = lambda ls: ls if isinstance(ls, (tuple, list)) else ls.tolist()
        # 辞書paramsを定義
        # 中身は、引数をリスト化したもの
        params = {
            "means": to_list(means),
            "stds": to_list(stds)
        }
        # JSONデータを1行文字列化
        serialized = json.dumps(params)
        # インスタンス変数param_fileの指すファイルをバイナリ書き込みで開く
        with open(self.param_file, "wb") as f:
            # paramsの1行文字列化データをUTF-8でファイルへ書き込む
            f.write(serialized.encode("utf-8"))

    # 正規化パラメータをファイルからロード
    # 引数 なし
    # 戻り値 means: 復元したmeans配列
    # 戻り値 stds: 復元したstds配列
    #
    # param_fileが指すファイルを開きUTF-8型式で読み込み配列として返却
    def load_normalization_params(self):
        loaded = {}
        if not os.path.isfile(self.param_file):
            raise Exception("Normalization parameter file does not exist.")
        # param_fileが指すファイルを　バイナリ読み込むモードで開く
        with open(self.param_file, "rb") as f:
            # UTF-8型式で読み込みJSONデータ(辞書)としてloaded変数へ格納
            loaded = json.loads(f.read().decode("utf-8"))
        # 引数値を配列化する関数を定義
        to_array = lambda x: np.array([float(_x) for _x in x], dtype=np.float32)
        # meansの復元値配列、stdsの復元値配列を返却
        return to_array(loaded["means"]), to_array(loaded["stds"])
    # トレーニングデータをロード
    # 引数なし
    # 戻り値 x: 復元したトレーニングデータのinput
    # 戻り値 y: 復元したトレーニングデータのoutput
    #
    # トレーニングデータを読み込み、戻り値として返却する
    # 本コードをコピペで流用する場合はこの関数を書き換え、
    # ローカルファイル上のファイルを読み込み、戻り値化する実装に変更する
    def load_training_data(self):
        # scikit-learnに用意されているMNISTデータを使用
        from sklearn.datasets import load_digits
        # predifine set is from scikit-learn dataset
        # http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html

        digits = load_digits()
        x = digits.data
        y = digits.target

        return x, y

    # データを保存する
    # 引数 path: 保存先ファイルのパス
    # 引数 data: 保存対象のデータ（0番目：ラベル、1番目以降：浮動小数点数）
    #
    # 引数dataを引数pathが指すファイルへ追加書き込みする
    def save_data(self, path, data):
        # 引数pathの指すファイルを追加書き込みバイナリモードで開く
        with open(path, "ab") as f:
            # data[0]→int化してlabel変数へ
            # data[1,2,...]→float化してfeatures配列へ
            label = int(data[0])
            features = [float(d) for d in data[1:]]
            # features配列長がINPUT_SIZEより大きい場合
            if len(features) > self.INPUT_SIZE:
                # data_processor.py上のDataProcessorクラスを生成
                dp = DataProcessor()
                # INPUT_SIZE長の配列に調整してfreatures配列へ格納
                features = dp.adjust(np.array([features]), self.INPUT_SIZE).tolist()[0]
            # features配列長がINPUT_SIZEより小さい場合
            elif len(features) < self.INPUT_SIZE:
                # 例外を発生
                raise Exception("Size mismatch when saving the data.")
            # ラベル、features配列をタブでセパレートした文字列＋改行
            line = "\t".join([str(e) for e in [label] + features]) + "\n"
            # UTF-8型式で保存
            f.write(line.encode("utf-8"))

    # データをロードする
    # 引数 path: 保存先ファイルのパス
    # 戻り値 x: np.ndarray型式の配列（feature配列値）
    # 戻り値 y: np.ndarray型式の配列（label値を要素1の配列化したもの）
    #
    # 引数pathが指すファイルから読み込み、
    # np.ndarray型式の浮動小数点配列化して返却する
    def load_data(self, path):
        x = []
        y = []
        with open(path, mode="r", encoding="utf-8") as f:
            for line in f:
                # 改行を含めた空白文字を両端から除去
                line = line.strip()
                # read_data関数を呼び出し、label(最初の要素)、
                # features配列(2番め以降の要素を配列化)化する
                label, features = self.read_data(line)
                # features配列化
                x.append(features)
                # 変数yを要素１の配列にしてlabel値を保存
                y.append(label)
        # np.ndarrya型式の配列に変えて、返却
        x = np.array(x, dtype=np.float32)
        y = np.array(y, dtype=np.float32)
        return x, y

    # TSV型式１行文字列をラベルとfeatures配列に切り出す
    # 引数 line: 処理対象の文字列（１行を表す文字列、改行なし）
    def read_data(self, line):
        # タブで切り出す
        elements = line.split("\t")
        # 最初の要素だけint化してラベルに
        label = int(elements[0])
        # のこりはfloat化して配列化しラベルと一緒に返却
        features = [float(e) for e in elements[1:]]
        return label, features

    # モデルを保存する
    # 引数 model:
    # 戻り値なし
    #
    # インスタンス変数model_pathが指すディレクトリの下に
    # <小文字化したモデルのクラス名>_<YYYYmmddHHMMSS型式の現在日付>.model と
    # いうファイル名で保存する
    # chainerライブラリを使っているので別のライブラリを使用する場合は書き換える
    # 必要がある
    def save_model(self, model):
        # インスタンス変数model_pathが指すディレクトリが存在しない場合
        if not os.path.exists(self.model_path):
            # ディレクトリを作成する
            os.mkdir(self.model_path)
        # ファイル名
        # <小文字化したモデルのクラス名>_<YYYYmmddHHMMSS型式の現在日付>.model 
        # の先頭にディレクトリパスを挿入
        timestamp = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        model_file = os.path.join(self.model_path, "./" + model.__class__.__name__.lower() + "_" + timestamp + ".model")
        # chainerライブラリの保存関数をつかって保存する
        serializers.save_npz(model_file, model)

    # モデルをロードする
    # 引数 model: modelクラスインスタンス(chainer.Chainサブクラス)
    # 戻り値なし
    #
    # インスタンス変数model_pathが指すディレクトリの下の最新のファイルを
    # 使って引数modelの状態を復元する
    # chainerライブラリを使っているので別のライブラリを使用する場合は書き換える
    # 必要がある
    def load_model(self, model):
        # インスタンス変数 model_path の指すディレクトリが存在しない場合
        if not os.path.exists(self.model_path):
            # 例外を発生
            raise Exception("model file directory does not exist.")

        # model_path 内の <モデルクラス名の小文字化>*.model というファイル
        # のなかで最も日時が最新のファイル名を見つけ変数model_fileへ格納
        suffix = ".model"
        keyword = model.__class__.__name__.lower()
        candidates = []
        for f in os.listdir(self.model_path):
            if keyword in f and f.endswith(suffix):
                candidates.append(f)
        candidates.sort()
        latest = candidates[-1]
        #print("targets {}, pick up {}.".format(candidates, latest))
        model_file = os.path.join(self.model_path, latest)
        # chainerライブラリのロード関数を使って状態を復元する
        serializers.load_npz(model_file, model)
