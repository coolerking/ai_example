# -*- coding: utf-8 -*-
'''アプリケーション側とモデル側のファサードとなるモジュール。
(C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
'''
__author__ = 'Tasuku Hori'

# ml/model.py 上の Wakatigaki クラスを使用
from ml.model import Wakatigaki

class ModelAPI():
    '''推測側アプリケーションに対するモデルファサードクラス。
    '''

    def __init__(self, resource):
        '''モデルインスタンスを生成。
        '''

        self.resource = resource
        self.model = Wakatigaki()
        # モデルを復元する(Wakatigakiは学習不要なので形だけ)
        resource.load_model(self.model)

    def predict(self, data):
        '''分かち書き済みテキストを返却。
        '''
        
        # 引数dataがlistかtupleである場合
        if isinstance(data, (list, tuple)):
            sentence = "".join(data)
        # list,tuple以外の場合
        else:
            sentence = data
        return self.model(sentence)
