# -*- coding: utf-8 -*-
'''モデルモジュール。
モデルが使用するライブラリ固有の操作を隠蔽する。
(C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
'''
__author__ = 'Tasuku Hori'

# janome を使用 http://mocobeta.github.io/janome/
from janome.tokenizer import Tokenizer


class Wakatigaki():
    '''分かち書きモデルクラス。
    '''

    def __init__(self):
        '''janomeのTokenizerをインスタンス化する。
        '''
        self.t = Tokenizer()

    def __call__(self, sentence, separator=" "):
        '''Tokenizerを使って分かち書き化する。
        引数sentenceに渡された文字列をjanomeで処理した結果を
        1つの文字列にもどして返却する。
        引数separatorを指定することで、返却時の単語間にはさむ文字を
        変更することができる。
        '''

        malist = self.t.tokenize(sentence)
        r = separator.join([w.surface for w in malist]).strip()
        return r
