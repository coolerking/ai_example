# coding: -*- utf-8 -*-
import numpy as np
from ml.model import NumberRecognizeNN
from ml.data_processor import DataProcessor

# ModelAPIクラス
#
# 予測を行うアプリは、このAPI経由でモデルをあつかわせる
class ModelAPI():
    # コンストラクタ相当の関数
    # 引数 resource: Resourceクラスインスタンス
    #
    # インスタンス変数 resource、model（学習済みモデル）、dpの初期化を行う
    def __init__(self, resource):
        # 引数resourceで渡されたResourceクラスをインスタンス変数resourceへ格納
        self.resource = resource
        # モデルクラスNumberRecognizeNNを生成しインスタンス変数modelへ格納
        # コンストラクタ引数にResourceクラスのインスタンス遍数resourceを使用
        self.model = NumberRecognizeNN(resource.INPUT_SIZE, resource.OUTPUT_SIZE)
        # ファイルを読み込み、モデルクラスを最新の学習状況に復元する
        resource.load_model(self.model)

        # 平均値パラメータ、標準偏差パラメータもファイルから復元する
        means, stds = resource.load_normalization_params()
        # DataProcessorインスタンスを生成し、インスタンス変数dpへ
        self.dp = DataProcessor(means, stds)

    # 予測を行う
    # 引数 data: 入力データ
    # 戻り値: 識別数字（0～9）
    #
    # インスタンス変数上のモデルを使って予測を実行し、
    # 予測確率の高い識別数字を返却する
    def predict(self, data):
        # data がタプルかリストの場合、要素がfloat32のnp.ndarryへ
        _data = data
        if isinstance(data, (tuple, list)):
            _data = np.array([data], dtype=np.float32)

        # DataProcessorを使ってモデルが受付可能な入力データ化する
        f_data = self.dp.format_x(_data, size=self.resource.INPUT_SIZE)
        # インスタンス変数上のモデルインスタンスを使って予測実行
        predicted = self.model(f_data)
        # np.argmaxは最大値となる要素のインデックスを返す関数
        # np.maxは単に最大値を求めているだけ
        # predicted.data 配列はインデックス番号が識別対象数値になっている
        number = np.argmax(predicted.data, axis=1)
        # 予測確率が最も高い識別数値として返却
        return number
