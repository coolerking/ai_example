# coding: -*- utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import unittest
import shutil
import numpy as np
from ml.model import NumberRecognizeNN
from ml.data_processor import DataProcessor
from ml.trainer import Trainer
from ml.resource import Resource

# Trainerクラスのテストクラス(unittest.TestCase継承)
#
# テストしたい場合は、python test_trainer.py を実行する
# Trainer#train()が例外なく実行できるか、
# sklearnのSVCのaccuracyはどのくらいになるかを表示するだけで
# 実はきちんとしたテストクラスになっていない
class TestTrainer(unittest.TestCase):
    # クラス変数：テストディレクトリ
    TEST_DIR = ""

    # テスト開始時１度だけ処理される
    # クラスメソッド宣言
    @classmethod
    # クラスメソッドの第1引数にはクラスが渡される→クラス変数にはアクセス可能
    # インスタンス変数にはアクセスできないがクラス変数にはアクセスできる
    def setUpClass(cls):
        # 実行ディレクトリ + "./test_trainer"
        path = os.path.join(os.path.dirname(__file__), "./test_trainer")
        # ディレクトリが無い場合
        if not os.path.isdir(path):
            # ディレクトリ作成
            os.mkdir(path)
        # クラス変数へ格納
        cls.TEST_DIR = path

    # テスト終了時１度だけ処理される
    # クラスメソッド宣言
    @classmethod
    # クラスメソッドの第1引数にはクラスが渡される→クラス変数にはアクセス可能
    # インスタンス変数にはアクセスできないがクラス変数にはアクセスできる
    def tearDownClass(cls):
        # ディレクトリが存在する場合
        if os.path.isdir(cls.TEST_DIR):
            # ディレクトリツリー全体を削除
            shutil.rmtree(cls.TEST_DIR)

    # インスタンスメソッド：テストメソッド
    # インスタンスメソッドは引数で自分自身のインスタンスをうけとれる
    #
    # トレーニングが例外なく正常動作するかのテスト
    def test_train(self):
        # モデルクラスNumberRecognizeNNのインスタンス生成
        model = NumberRecognizeNN(Resource.INPUT_SIZE, Resource.OUTPUT_SIZE)
        # リソースクラスのインスタンスを生成する
        # root値を指定してテスト中に作成される各種保存ファイルパスを変えている
        r = Resource(self.TEST_DIR)
        # トレーナクラス（テスト対象）のインスタンスを生成
        trainer = Trainer(model, r)
        dp = DataProcessor() #? 使ってない、コピペの残骸？
        # トレーニングデータをロードする
        data, target = r.load_training_data()
        print("Test Train the model")
        # モデルに対してトレーニングを実施し、モデル状態をファイルへ保存する
        trainer.train(data, target, epoch=5)
        # アプリケーションでも最初はここまで実行される(ただしepochは200)

    # インスタンスメソッド：テストメソッド
    # インスタンスメソッドは引数で自分自身のインスタンスをうけとれる
    #
    # ベースラインシステムとしてsklearnのSVCを200件データでトレーニングした
    # accuracyを標準出力に表示するだけで、実際はテストになっていない
    def test_baseline(self):
        # サポートベクタマシンをベースラインシステムに指定
        from sklearn.svm import SVC
        from sklearn.metrics import accuracy_score
        # リソースクラスのインスタンスを生成する
        # root値を指定してテスト中に作成される各種保存ファイルパスを変えている
        r = Resource(self.TEST_DIR)
        dp = DataProcessor()
        # トレーニングデータをロードする
        data, target = r.load_training_data()
        # DataProcessorインスタンス遍数の正規化パラメータ群を初期化
        dp.set_normalization_params(data)
        # モデルが受け付けるように入力データ、出力データを編集
        f_data, f_target = dp.format_x(data), dp.format_y(target)

        # テスト件数は先頭200件
        test_size = 200
        # サポートクタマシンをそのまま使用
        model = SVC()
        # sklearn のトレーニングはfitを実行する
        model.fit(f_data[:-test_size], f_target[:-test_size])

        # 残りのデータをテスト用に使用
        predicted = model.predict(f_data[-test_size:])
        teacher = f_target[-test_size:]
        # accuracyスコアを取得し、標準出力へ表示
        score = accuracy_score(teacher, predicted)
        print("Baseline score is {}".format(score))

# コマンドラインから python test_trainer.py で実行された際に
# テストを開始する
if __name__ == "__main__":
    unittest.main()

