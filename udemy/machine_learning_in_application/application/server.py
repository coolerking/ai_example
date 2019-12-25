# coding: -*- utf-8 -*-
# パス操作のためにosパッケージをインポート
import os
# tornado フレームワークをインポート
import tornado.web
# ml\model_api.oy内のModelAPIクラスをインポート
from ml.model_api import ModelAPI
# ml\data_proxcessor.py 内の DataProcessorクラスをインポート
from ml.data_processor import DataProcessor
# ml\resource.py 内の Resourceクラスをインポート
from ml.resource import Resource

# フィードバックデータファイルのフルパス
# HTTPパラメータのキー"data[]"値をファイルへ追加書き込みしていく
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/feedbacks.txt")

# "/":インデックスハンドラ
# tornado.web.RequestHandlerクラスを継承
class IndexHandler(tornado.web.RequestHandler):
    # GETメソッド通信
    def get(self):
        # "index.html"をレスポンスとしてレンダリング
        self.render("index.html", title="title")

# "/predict":予測ハンドラ
# tornado.web.RequestHandlerクラスを継承
class PredictionHandler(tornado.web.RequestHandler):
    # POSTメソッド通信
    def post(self):
        # 辞書respを初期化
        resp = {"result": str(-1)}
        # Requestパラメータなどデータを取得
        data = self.get_arguments("data[]")

        # ml.Resourceクラスの生成
        r = Resource()
        # モデルデータ保存ディレクトリが無い場合
        if not os.path.isdir(r.model_path):
            # ../ml/model/model.py 上のNumberrecognizeNNクラスをインポート
            from ml.model import NumberRecognizeNN
            # ../ml/model/trainer.py 上のTrainerクラスをインポート
            from ml.trainer import Trainer
            # NumberRecognizeNNクラスをインスタンス化する
            # モデルのinput次元、output次元はResourceクラスの
            # 各インスタンス変数を使う
            model = NumberRecognizeNN(r.INPUT_SIZE, r.OUTPUT_SIZE)
            # トレーニングクラスを生成する
            trainer = Trainer(model, r)
            # トレーニングデータをファイル（実際にはネット）から読み込む
            x, y = r.load_training_data()
            # トレーニングを実行する（最新モデル状態はファイルに保存）
            trainer.train(x, y)
        # ModelAPIクラスを生成する
        api = ModelAPI(r)

        # data配列件数が1以上の場合
        if len(data) > 0:
            # 配列要素をfloat化
            _data = [float(d) for d in data]
            # 配列を入力データとして、予測を実行する
            predicted = api.predict(_data)
            # 結果を文字列化して辞書respの"result"値へ格納
            resp["result"] = str(predicted[0])

        # 辞書respをHTTPパラメータへ書き込み
        self.write(resp)

# "/feedback":フィードバックハンドラ
# tornado.web.RequestHandlerクラスを継承
class FeedbackHandler(tornado.web.RequestHandler):
    # POSTメソッド通信
    def post(self):
        # キー"data[]"のHTTPパラメータ値を取得
        data = self.get_arguments("data[]")
        # dataの要素数が1以上である場合
        if len(data) > 0:
            # クラスResourceを生成
            r = Resource()
            # data値をDATA_PATHの指すファイルへ上書き
            r.save_data(DATA_PATH, data)
        else:
            result = "feedback format is wrong."

        # キー"result"のHTTPパラメータを空文字化して書き込む
        resp = {"result": ""}
        self.write(resp)

# Applicationクラス
# tornado.web.Allication クラスを継承
# run_application.py でHTTP Serverとして登録される
class Application(tornado.web.Application):

    # コンストラクラ
    def __init__(self):
        # ハンドラリスト作成
        # [x,x,..]はリスト：要素後付編集可能
        # URL末尾文字列に対応するハンドラクラスを指定するためのhandlerリスト
        handlers = [
            # r"～" はraw文字列：エスケープ文字は通常文字として認識
            # (x,x,..)はタプル：要素を変更できない
            # 第0番目要素：URL末尾文字列、第1番目要素：ハンドラクラス
            (r"/", IndexHandler),
            (r"/predict", PredictionHandler),
            (r"/feedback", FeedbackHandler),
        ]

        # 設定辞書作成
        # dict(x,x,..)は辞書(の生成、{x:y,x:y,..})：キーと値のペアを格納
        settings = dict(
            # os.path.dirname(__file__)：カレントディレクトリ
            #  → machine_learning_in_application/application
            # template_path=
            #  "../machine_learning_in_application/application/templates"
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            # static_path=
            #  "../machine_learning_in_application/application/static"
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # os.environ.get():環境変数名が第１引数である値を返却、なければ
            #  第２引数の値を返却
            # cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"
            cookie_secret=os.environ.get("SECRET_TOKEN", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"),
            xsrf_cookies=True,
            debug=True,
        )

        # 親クラスのコンストラクタ
        # tornado.web.Application#__init__(self, ..) を呼び出し
        # ハンドラ、設定辞書を引数として渡す
        super(Application, self).__init__(handlers, **settings)
        # →port で指定したポート番号でHTTP待受、URLによりハンドラへ振り出し
