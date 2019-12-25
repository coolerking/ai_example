# coding: -*- utf-8 -*-
import chainer
import chainer.functions as F
import chainer.links as L

# NumberRecognizeNN(数値識別ニューラルネットワーク)クラス
# 関数っぽく実行するとモデルを通すことになるように実装する
# Chainer独自実装で内包されているため、別のライブラリを使用する場合
# 中身はほぼ書き換えとなる
class NumberRecognizeNN(chainer.Chain):

    # インスタンス生成時処理される（コンストラクタ相当）
    # 引数 input_size: 入力データベクトル次元数(画像データ総ピクセル数)
    # 引数 output_size: 出力データベクトル次元数(要素数)
    # 引数 hidden_size: 隠れ層の入出力サイズ、デフォルト200
    # 引数 layer_size: 層数、デフォルト3
    def __init__(self, input_size, output_size, hidden_size=200, layer_size=3):
        # すべての引数をインスタンス変数へ格納
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.layer_size = layer_size
        # 親クラスchainer.Chainの__init()__を実行する
        # 引数に各層の定義
        # L.Liner 全結合層：隣接そうのユニット同士が全結合するK^n_nグラフ状の
        # 層、重みやバイアスはLinearインスタンスが直接保持
        super(NumberRecognizeNN, self).__init__(
            l1=L.Linear(self.input_size, hidden_size),
            l2=L.Linear(hidden_size, hidden_size),
            l3=L.Linear(hidden_size, self.output_size),
        )

    # NumberRecognizeNN を実行する
    # 引数 x: 入力データ
    # 戻り値 o: 出力データ（予測データ）
    #
    # 入力データに対し、
    # 線形パーセプトロン→ReLU→線形パーセプトロン→ReLU→線形パーセプトロン
    # →sigmoid 処理した結果を予測データとして返す
    def __call__(self, x):
        # 各層の結果に活性化関数を最後に実行
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        o = F.sigmoid(self.l3(h2))
        return o
