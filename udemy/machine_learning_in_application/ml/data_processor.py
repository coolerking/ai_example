# coding: -*- utf-8 -*-
import numpy as np

# データ処理クラス
#
# データ処理ユーティリティとして使用される
# インスタンス変数 means: 入力データの平均値
# インスタンス遍数 stds: 入力データの標準偏差
class DataProcessor():

    # コンストラクタ相当の関数
    # 引数 means: デフォルト空のタプル（上書きできないリストの様なもの）
    # 引数 stds: デフォルト空のタプル
    #
    # 各引数値をインスタンス変数群へ格納する
    def __init__(self, means=(), stds=()):
        self.means = means
        self.stds = stds

    # 入力データフォーマット関数
    # 引数 x: 入力データ
    # 引数 size: プーリング後の次元数、デフォルト-1
    #
    # プーリング処理をかけ、means値を引いてstds値で割った値を返却する
    # size値が 0以下の場合などはプーリング処理をかけない
    def format_x(self, x, size=-1):
        # 引数をローカル変数_xで受け取る
        _x = x
        # x がタプルかリストである場合
        if isinstance(x, (tuple, list)):
            # np.npdarray型式へ変換し_xへ格納
            _x = np.array([x])
        # 引数sizeが正かつ_x の２番めの要素の次元がsize値と違う場合
        if size > 0 and _x.shape[1] != size:
            # 引数xに対してプーリン処理による調整をかけた結果を_xへ
            _x = self.adjust(x, size)
        # 要素をすべてfloat32型に変換
        _x = _x.astype(np.float32, copy=False)

        # インスタンス変数meansの長さ、インスタンス変数stdsの長さがともに
        # 0より大きい場合
        if len(self.means) > 0 and len(self.stds) > 0:
            # _xからmeansを引きstdsで割った値(float32)を返却
            return (_x - self.means) / self.stds
        # インスタンス変数meansの長さ、インスタンス変数stdsの長さのどちらかが
        # 0以下の場合
        else:
            # _xをそのまま返却
            return _x

    # 入力データの調整を行う関数
    # 引数 x: 入力データ
    # 引数 size: 各入力データの次元数
    # 戻り値 x: 調整済み入力データ
    #
    # 引数で与えられた入力データの次元をsize値に調整して返却する
    def adjust(self, x, size):
        # 関数内関数 max_pooling
        # 引数 v:アウトプット
        # 戻り値: np.ndarray型式、プーリング処理後のアウトプット
        #
        # リスト状の変数vに対してプーリング処理(kmax pooling)をかけ返却する
        def max_pooling(v):
            # 関数 sqrt(_x)をlambda式で定義
            # 引数 _x: リストライクな変数
            # 戻り値: _xの各要素の平方根の上限整数値化したもの
            sqrt = lambda _x: int(np.ceil(np.sqrt(_x)))
            # size値を上記のsqrt関数で平方根化する
            _target_square_size = sqrt(size)
            # 引数vの長さの平方根を上記sqrt関数で取得
            square_size = sqrt(len(v))
            # 引数vの平方根 と 親関数の引数sizeの平方根で切り捨て割り算(int)
            conv_size = int(square_size // _target_square_size)
            # 引数vの値を、引数vの長さの平方根×引数vの長さの平方根 の行列化
            image = np.reshape(v, (square_size, square_size))
            # ローカル変数 _pooled を空のリストで初期化
            _pooled = []
            # iを0からsize-1までループ
            # conv_size×conv_sizeのウィンドウでmax pooling処理し、結果を
            # リスト _pooled へ格納
            # →引数vに対してプーリング層の処理を実行し、結果リストを作成する
            for i in range(size):
                # 変数row:
                # 0, 0,..(_target_square_size数).., 0, 
                # conv_size, conv_size, ..(_target_square_size数).., conv_size,
                # conv_size*2, conv_size*2, ..
                # (_target_square_size数).., conv_size*size/_target_square_size
                # 変数col:
                # 0,conv_size,conv_size*2,..,conv_size*(_target_square_size-1),
                # 0,conv_size,conv_size*2,..,conv_size*(_target_square_size-1),
                # ..
                row, col = int(i // _target_square_size * conv_size), int(i % _target_square_size * conv_size)
                # conv_size×conv_sizeのウィンドウで最大の要素値を変数mpへ
                mp = np.max(image[row:row + conv_size, col: col + conv_size])
                # _poooled リストの最後の要素として追加
                _pooled.append(mp)
            # max_pooling処理結果を返却
            return np.array(_pooled)
        # 引数xを上記のmax pooling関数を使ってプーリング処理にかけ返却する
        x = np.array([max_pooling(_v) for _v in x])
        return x

    # 出力データを要素がint32で要素数1のnp.ndarray型配列に変換する関数
    # 引数 y: 出力データ
    # 戻り値: 変換後np.ndarray型配列
    def format_y(self, y):
        _y = y
        # 引数yがintの場合
        if isinstance(y , int):
            # 要素数１のnp.ndarry配列化
            _y = np.array([y])
        # _yの要素をint32型に変換
        _y = _y.astype(np.int32, copy=False)
        # 要素がint32で要素数1のnp.ndarray型配列に変換して返却
        return _y 

    # 正規化パラメータをインスタンス変数群にセットする関数
    # 引数 x: 入力データ
    # 戻り値なし(インスタンス変数means、stds更新)
    #
    # インスタンス変数meansとstdsを正規化パラメータ値をセットスル
    def set_normalization_params(self, x):
        # np.means関数: 平均値を求める(avergeと違って重み付け対応していない)
        # x: 配列ライクな変数、平均値を求める対象となる
        # axis: 軸、どの軸に沿って平均を求めるか
        # dtype: 平均を求める際に使用するデータ型
        # 返却値: x要素の(axisを軸とした)平均値をdtypeで指定した型で返却

        # インスタンス変数値means
        # ← xの全要素の平均を0を軸としてfloat32型式で求める
        self.means = np.mean(x, axis=0, dtype=np.float32)

        # np.std関数: 標準偏差を求める
        # x: 配列ライクな変数、標準偏差を求める対象となる
        # axis: 軸、どの軸に沿って平均を求めるか
        # dtype: 標準偏差を求める際に使用するデータ型
        # 返却値: x要素の(axisを軸とした)標準偏差をdtypeで指定した型で返却

        # インスタンス変数値 stds
        # ← xの全要素の0を軸とした標準偏差をfloat32型式で求める
        self.stds = np.std(x, axis=0, dtype=np.float32)

        # simple trick to avoid 0 divide
        # 0で割ることを避ける簡単なトリック

        # stds値が1.0e-6より大きい場合は最初の要素に、
        # stds値が1.0e-6未満の場合は2番めの要素に、
        # xの最大値から最小値を格納
        self.stds[self.stds < 1.0e-6] = np.max(x) - np.min(x)
        # means値が1.0e-6より大きい場合は最初の要素に、
        # means値が1.0e-6未満の場合は2番めの要素に、
        # xの最小値を格納
        self.means[self.stds < 1.0e-6] = np.min(x)

    # バッチイテレータ
    # 引数 X: 入力データ
    # 引数 y: 出力データ(正解データ)
    # 引数 batch_size: バッチサイズ
    # 引数 epoch: バッチ回数、デフォルト1回
    # 戻り値 x_batch: バッチ1回分の入力データ
    # 戻り値 y_batch: バッチ1回分の出力データ（正解データ）
    # 戻り値 epoch_end: epoch の終わりかどうかの真偽値
    def batch_iter(self, X, y, batch_size, epoch=1):
        # np.ndarray配列 [0, 1, 2,.., (出力データの要素数-1)]
        indices = np.array(range(len(y)))
        # batch_size から 出力データ要素数をbacht_sizeで割ったあまりで引いた数
        appendix = batch_size - len(y) % batch_size
        # e ← 0, 1, .., (出力データの要素数-1)
        for e in range(epoch):
            # np.ndarray配列 [0, 1,.. (出力データの要素数-1)]の要素をシャッフル
            np.random.shuffle(indices)
            # シャッフル済みの配列に
            # シャッフル済みの配列(要素先頭からappendix件まで)を連結したもの
            batch_indices = np.concatenate([indices, indices[:appendix]])
            # batch_size←(出力データの要素数+appendix)をbatch_sizeで
            # 切り捨て除算
            # バッチ件数
            batch_count = len(batch_indices) // batch_size
            # b ← 0, 1, ..  , バッチ件数-1
            for b in range(batch_count):
                # b+1回目のバッチデータを切り出し、入力・出力データの要素位置を
                # batch_indicesから取り出す
                elements = batch_indices[b * batch_size:(b + 1) * batch_size]
                # 要素位置elementをバッチ1件分データとして切り出す
                x_batch = X[elements]
                y_batch = y[elements]
                # b の値が最後の場合 True、そうではない場合 False
                epoch_end = True if b == batch_count - 1 else False
                # この段階で戻り値を返す
                # 次回呼び出した場合は、この行の次（for b..の次か for e..の次)
                # を実行する（pythonのyield機能）
                yield x_batch, y_batch, epoch_end
