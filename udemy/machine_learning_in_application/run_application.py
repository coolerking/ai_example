# coding: -*- utf-8 -*-
import os
# tornado は python で動作するWebフレームワーク
import tornado.ioloop
import tornado.httpserver
import tornado.escape
from tornado.options import define, options
from application.server import Application

# コマンドライン引数定義
## port : サーバ待受ポート番号
define("port", default=3000, help="run on the given port", type=int)

# メイン関数
#
# Python tornado フレームワークを使ったWebアプリケーションを
# 環境変数PORTで指定されたポート番号で待ち受ける
# Webアプリケーション本体（HTTPメソッドのハンドラ指定）は
# application\server.py 内のApplicationクラスやハンドラクラス群を
# 参照すること
def main():
    # すべてのオプションをコマンドラインから読み取り sys.argv へ
    # tornado.options.parse_command_line()
    # application/servers.py#ApplicationクラスをHTTP Serverへセット
    http_server = tornado.httpserver.HTTPServer(Application())
    # 環境変数"PORT"の値、なければoptions.port=3000を変数portへセット
    port = int(os.environ.get("PORT", options.port))
    # ポート番号を標準出力へ表示
    print("server is running on port {0}".format(port))
    # port 番号でHTTP Server待受設定
    http_server.listen(port)
    # 待受の開始
    tornado.ioloop.IOLoop.current().start()

# コマンドラインからスクリプトファイルを指定してpythonインタプリタ
# を起動すると __main__ という名前のモジュールとしてpythonに読み込まれる
# →本ファイルをスクリプトファイル指定で実行された場合、関数main()を実行する
if __name__ == "__main__":
    try:
        main()
    # 例外発生時はstdoutへ出力して終了
    except Exception as ex:
        print(ex)
