# -*- coding: utf-8 -*-
'''アプリケーション側とモデル側のファサードとなるモジュール
(C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
'''

# ml/model.py 上の Word2Vec クラスを使用
from ml.model import Word2Vec

import json

class ModelAPI():
    '''推測側アプリケーションに対するモデルファサードクラス
    '''
    
    # クラスロード時にモデルクラスを生成する
    model = Word2Vec()

    def __init__(self, resource):
        '''Resourceおよびモデルをインスタンス変数へ格納
        '''
        self.resource = resource
        self.model = ModelAPI.model

    def predict(self, data):
        '''モデルを使った予測結果を返却
        '''
        s = self.model(data)
        if len(s) == 0:
            return [{'id':0, 'text':'＜該当なし＞', 'probability':1.0}]
        return [ { 'id':i, 'text':_s[0], 'probability':_s[1]} for i,_s in enumerate(s)]