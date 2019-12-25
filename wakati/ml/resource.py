# -*- coding: utf-8 -*-
'''リソースを管理するモジュール。
このモジュールとmodel_api.pyがアプリケーションとの境界として働く。
(C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
'''
__author__ = 'Tasuku Hori'

class Resource():
    ''' リソースクラス。
    分かち書きの場合、扱うものがない。
    '''

    def __init__(self):
        ''' コンストラクタ。
        実装なし。
        '''

        pass

    def load_model(self, model):
        ''' Resourceクラス上の情報をもとに
        modelクラスへ学習済みパラメータを復元させる。
        しかし、分かち書きの場合は実装がない。
        '''

        pass