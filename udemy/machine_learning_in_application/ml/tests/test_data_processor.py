# coding: -*- utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import math
import unittest
import numpy as np
from ml.resource import Resource
from ml.data_processor import DataProcessor

# DataProcessorをテストするためのクラス(unittest.TestCase継承)
#
# DataProcessorはそれなりにテストしているが、疎通レベルの正常動作のみ
# のテストケースしかない
class TestDataProcessor(unittest.TestCase):
    # format_x() テストメソッド
    #
    # 引数sizeを指定しない場合の正常動作確認テスト
    def test_format_x(self):
        # テスト用means/stds値
        means = np.array([0, 0.1, 0.2])
        stds = np.array([1, 1.5, 0.5])
        # DataProcessor#init() を実行してインスタンス変数へ
        dp = DataProcessor(means=means, stds=stds)
        # テスト用データ
        data = np.array([[1, 2, 3], [4, 5, 6]])
        # テスト対象メソッド実行
        x = dp.format_x(data)
        # 結果のアサーション
        _x = (data - means) / stds
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                self.assertEqual(x[i][j], _x[i][j])

    # format_x() テストメソッド
    #
    # 引数sizeを指定した場合の正常動作確認テスト
    # テストデータがsizeで割り切れない要素数配列の場合のテストになる
    def test_format_x_resize(self):
        # means/stds値は正規化パラメータ用を使用
        dp = DataProcessor()
        # 15件のテストデータ
        data = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]])
        # sizeを4にしてテスト対象メソッドを実行
        x = dp.format_x(data, size=4)
        # 想定値になっているかアサーションを実行
        v = x[0].tolist()
        self.assertEqual(v[0], 6)
        self.assertEqual(v[1], 8)
        self.assertEqual(v[2], 14)
        self.assertEqual(v[3], 16)

    # batch_iter() テストメソッド
    #
    # バッチ切り出しの要素数、epoch_endの真偽値、バッチカウント数が
    # 正しいかを確認するテスト(batch_size=10)
    def test_batch_iter(self):
        batch_size = 10
        dp = DataProcessor()
        r = Resource()
        train_x, train_y = r.load_training_data()
        batch_count = math.ceil(len(train_y) / batch_size)

        i = 0
        for x_batch, y_batch, epoch_end in dp.batch_iter(train_x, train_y, batch_size):
            self.assertEqual(batch_size, len(x_batch))
            self.assertEqual(batch_size, len(y_batch))
            if i < batch_count - 1:
                self.assertFalse(epoch_end)
            else:
                self.assertTrue(epoch_end)
            i += 1
        self.assertEqual(i, batch_count)

# python test_data_processor.py として実行した際の処理
if __name__ == "__main__":
    # テストフレームワーク実行
    unittest.main()

