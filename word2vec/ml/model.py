# -*- coding: utf-8 -*-
'''モデルモジュール。
モデルが使用するライブラリ固有の操作を隠蔽する。
(C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
'''
__author__ = 'Tasuku Hori'

# gensim を使用 https://radimrehurek.com/gensim/
from gensim.models import word2vec
from ml.resource import Resource

class Word2Vec():
    '''Word2Vecモデルクラス。
    '''
    
    # クラスをロードした時点で復元しておく
    model = word2vec.Word2Vec.load(Resource.store_path)

    def __init__(self):
        '''実際に使用するモデルをインスタンス変数へ格納
        '''
        self.model = Word2Vec.model

    def __call__(self, positive, negative=None):
        '''類似語検索を実行する。
        引数は共に単語リスト。
        引数positiveは必須、引数negativeはオプションとする。
        '''
        if negative == None:
            return self.model.most_similar(positive=positive)
        return self.model.most_similar(positive=positive, negative=negative)
