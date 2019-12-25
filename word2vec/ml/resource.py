# -*- coding: utf-8 -*-
'''リソースを管理するモジュール。
このモジュールとmodel_api.pyがアプリケーションとの境界として働く。
(C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
'''
__author__ = 'Tasuku Hori'

import os

class Resource():
    ''' リソースクラス。
    '''
    
    # クラス変数
    store_path = os.path.join(os.path.dirname(__file__), "store/jawiki.model")

    def __init__(self):
        ''' コンストラクタ。
        クラス変数をインスタンス変数化する。
        '''
        self.store_path = Resource.store_path