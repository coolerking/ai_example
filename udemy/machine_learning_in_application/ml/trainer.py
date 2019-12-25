# coding: -*- utf-8 -*-
import numpy as np
from sklearn.model_selection import train_test_split
# Chainer ライブラリを使用する
import chainer
# 損失関数としてSoftmaxクロスエントロピー関数を使う
from chainer.functions.loss import softmax_cross_entropy
# 評価関数にaccuracyを使う
from chainer.functions.evaluation import accuracy
# ml\data_processor.py内のDataProcessorをインポート
from ml.data_processor import DataProcessor

# トレーナークラス
class Trainer():

    # コンストラクタ相当の関数
    # 引数 model: モデルクラスインスタンス(ここではNumberRecognizeNN)
    # 引数 resource: リソースクラスインスタンス(ここではResource)
    # 戻り値なし
    #
    # 引数群をインスタンス変数群へ格納する
    def __init__(self, model, resource):
        self.model = model
        self.resource = resource

    # モデルに対してトレーニングを実施し、モデル状態をファイルへ保存する
    # 引数 data: 入力データ
    # 引数 target: 出力データ（正解データ）
    # 引数 batch_size: １epochのデータ件数、デフォルト100
    # 引数 epoch: epoch数、デフォルト5回
    # 引数 test_size: デフォルト0.3(3割をテストデータへ)
    # 引数 report_interval_epoch: レポート作成間隔、デフォルト1エポック
    def train(self, data, target, batch_size=100, epoch=5, test_size=0.3, report_interval_epoch=1):
        # データ処理ユーティリティクラスを生成
        dp = DataProcessor()
        # データ処理ユーティリティクラスのインスタンス変数を
        # 正規化パラメータで初期化
        dp.set_normalization_params(data)
        # データ処理ユーティリティクラスの正規化パラメータをファイルへ保存
        self.resource.save_normalization_params(dp.means, dp.stds)
        # 入力データdataに対してプーリング処理をかけ、
        # 平均値を引いて標準偏差値で割った値を返却する
        _data = dp.format_x(data)
        # 訓練データの出力データtargetを要素がint32で要素数1の
        # np.ndarray型配列に変換する
        _target = dp.format_y(target)
        # sklearn.model_selectionのtrain_test_split関数を使って、
        # _dataと_targetから、
        # 訓練データ(train_x, train_y)、テストデータ(test_x, test_y)
        # テストデータを全データのうちtest_sizeだけ振り分け
        train_x, test_x, train_y, test_y = train_test_split(_data, _target, test_size=test_size)

        # ChainerライブラリのオプティマイザクラスAdam()を生成
        optimizer = chainer.optimizers.Adam()
        # 毎回勾配配列をクリアする設定に変更
        optimizer.use_cleargrads()
        # 対象モデル(Chainerリンク)を設定して、オプティマイザを初期化する
        optimizer.setup(self.model)
        # loss関数をlamda式で定義
        # 引数 pred: 予測データ
        # 引数 teacher: 教師データ（正解データ）
        # 戻り値: softmax_cross_entropyによる交差エントロピー損失
        loss = lambda pred, teacher: softmax_cross_entropy.softmax_cross_entropy(pred, teacher)
        # batch_iterはバッチデータを１件分だけ取り出して返す
        # バッチの終わりの場合epoch_endにTrueが返ってくる
        for x_batch, y_batch, epoch_end in dp.batch_iter(train_x, train_y, batch_size, epoch):
            # モデルクラスの__call__を実行する
            # →1件分のバッチデータに対しモデルを実行し結果（予測データ）を取得
            predicted = self.model(x_batch)
            # 損失関数、予測データ、正解データを引数に与え最適化を実行
            optimizer.update(loss, predicted, y_batch)
            # epoc終わりの場合
            if epoch_end:
                # 現バッチデータのacuuracyを取得
                train_acc = accuracy.accuracy(predicted, y_batch)
                # 最適化後の状態でテストデータで予測
                predicted_to_test = self.model(test_x)
                # テストデータのacuuracyを取得
                test_acc = accuracy.accuracy(predicted_to_test, test_y)
                # accuracyをstdoutへ出力
                print("train accuracy={}, test accuracy={}".format(train_acc.data, test_acc.data))
                # Resourceクラスのモデル保存関数で現時点のモデル状態保存
                self.resource.save_model(self.model)
