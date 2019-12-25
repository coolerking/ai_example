# -*- coding: utf-8 -*-
'''コマンドライン起動するモジュール。
(C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
'''
__author__ = 'Tasuku Hori'

import os
import tornado.ioloop
import tornado.httpserver
import tornado.escape
from tornado.options import define, options
from application.server import Application

# デフォルトポート番号
define("port", default=3000, help="run on the given port", type=int)

def main():
    ''' Webアプリを起動する関数。
    ml/application.py 内の Application クラスにアプリ実装が存在。
    '''

    # サーバ待受ポート指定
    http_server = tornado.httpserver.HTTPServer(Application())
    port = int(os.environ.get("PORT", options.port))
    print("server is running on port {0}".format(port))
    http_server.listen(port)

    # 待受開始。
    tornado.ioloop.IOLoop.current().start()

# コマンドラインからモジュール実行された場合、main()を実行する。
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
