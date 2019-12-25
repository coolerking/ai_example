# -*- coding: utf-8 -*-
'''Web Applicationを定義するモジュール。
各HTTPリクエストに対するハンドラ群の定義もこの中に書かれている。
(C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
'''
__author__ = 'Tasuku Hori'

import os
import tornado.web
from ml.resource import Resource
from ml.model_api import ModelAPI


class IndexHandler(tornado.web.RequestHandler):
    ''' 初期画面表示ハンドラクラス。
    '''
    def get(self):
        ''' GET受信時、index.html を表示します。
        '''
        self.render("index.html", title="title")

class WakatiHandler(tornado.web.RequestHandler):
    ''' モデル実行ハンドラクラス。
    '''

    def post(self):
        ''' POST受診時、モデルのpredict()を呼び出し、
        結果を返却する（AJAXコールバックへ渡される）。
        '''
        # 辞書respを初期化
        resp = {"output_text": str(-1)}

        # Requestパラメータなどデータを取得
        # list型式で受領するため１件めを指定
        data = self.get_arguments("input_text")[0].split()

        # ml.Resourceクラスの生成
        r = Resource()
        
        # モデルへResourceを適用
        api = ModelAPI(r)
        
        # 予測実行
        predicted = api.predict(data)

        # 結果をパラメータとして保存
        resp["output_text"] = predicted

        # 辞書respをHTTPパラメータへ書き込み
        self.write(resp)

class Application(tornado.web.Application):
    '''Web Application をあらわすクラス。
    tornadoによるHTTPリクエストとイベントハンドラの紐付けを行う。
    '''

    def __init__(self):
        '''ハンドラリスト作成
        [x,x,..]はリスト：要素後付編集可能
        URL末尾文字列に対応するハンドラクラスを指定するためのhandlerリスト
        '''
        handlers = [
            # r"～" はraw文字列：エスケープ文字は通常文字として認識
            # (x,x,..)はタプル：要素を変更できない
            # 第0番目要素：URL末尾文字列、第1番目要素：ハンドラクラス
            (r"/", IndexHandler),
            (r"/predict", WakatiHandler),
        ]

        # 設定辞書作成
        # dict(x,x,..)は辞書(の生成、{x:y,x:y,..})：キーと値のペアを格納
        settings = dict(
            # テンプレートディレクトリ(htmlやテンプレートが格納されている)
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # static ディレクトリ(js, cssの親ディレクトリ)
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # cookieを使ったクロスサイトスクリプティング対策を実施。
            # index.js 内にも同じ文字列を埋め込んでいる。
            cookie_secret=os.environ.get("SECRET_TOKEN", "2|4cdb01ba|98d5046a0c427a2fff3dedc176606622|1506334362"),
            xsrf_cookies=True,
            # デバッグオプション
            debug=True,
        )

        ''' 親クラスのコンストラクタ
        tornado.web.Application#__init__(self, ..) を呼び出し、
        ハンドラ、設定辞書を引数として渡して、ハンドラをバインドする。
        '''
        super(Application, self).__init__(handlers, **settings)
