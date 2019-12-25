# -*- coding: utf-8 -*-
import gym
import numpy as np
import random
import tensorflow as tf
import matplotlib
# グラフを画像ファイルとして出力
matplotlib.use('Agg')

import matplotlib.pyplot as plt

# FrozenLake 問題 8x8
env = gym.make('FrozenLake8x8-v0')

# TensorFlow 計算モデル

# TensorFlowの初期化
tf.reset_default_graph


# 入力値を格納する変数
inputs1 = tf.placeholder(shape=[1, env.observation_space.n], dtype=tf.float32)
# 重み
# 学習しやすくするために分散を0.01として正規分布でランダムにセット
W = tf.Variable(tf.random_uniform([env.observation_space.n, env.action_space.n], 0, 0.01))
# Q値の計算値を格納する領域
Qout = tf.matmul(inputs1, W)
# 報酬値 Q値の推定値を最大にする指し手を返す
predict = tf.argmax(Qout, 1)
# Q値の推定値
nextQ = tf.placeholder(shape=[1,  env.action_space.n], dtype=tf.float32)
# 損失関数:2乗和誤差の平均値を取る
loss = tf.reduce_sum(tf.square(nextQ - Qout))
# トレーニングを行うアルゴリズムの指定：勾配降下法、学習レート0,1
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
# モデルの更新:損失関数を最小にするように更新させる
updateModel = trainer.minimize(loss)
# 計算モデル上の変数を初期化
init = tf.global_variables_initializer()

# パラメータ

# 割引率
y = 0.99
# 選択するアクションのパラメータe
e  = 0.1
# 試行回数
#num_episodes = 20000 # FloydHub gpu2 11min
num_episodes = 20000

# トレーニング

#ステップごとの報酬を格納するリスト
jList = []
# トータルの報酬を格納するリスト
rList = []

# TensorFlow セッション
with tf.Session() as sess:
    # 変数の初期化
    sess.run(init)
    # 試行ループ
    for i in range(num_episodes):
        # FrozenLakeの開始
        s = env.reset()
        # 報酬の累積和の初期化
        rAll = 0
        # Holeに落ちたらdieのd
        d = False
        # 1試行内のカウンタ(step()回数)
        j = 0
        # カウンタループ
        while j < 499:
            # カウンタ加算
            j += 1
            # 次の指し手を予測させる
            # predict: 一番大きな方向を指し示す
            # Qout: Q値の計算値
            # np.identity(env.observation_space.n)[s:s+1]: 単位行列のs番目の値を取り出す
            a, allQ = sess.run([predict, Qout], feed_dict={
                inputs1: np.identity(env.observation_space.n)[s:s+1]})
            
            # e-グリーディ法
            #  ランダムな指し手：exploreを入れる
            #  既にわかっている良い手を使うのはexploit
            
            # 1以下の値をランダムに取得し、それがεより小さい場合
            if np.random.rand(1) < e:
                # 指し手を提案させる
                a[0] = env.action_space.sample()
            # action を渡すと結果を返すメソッドstep()
            # 結果：新しい指し手、報酬の結果、指し手の結果穴に落ちたか
            s1, r, d, _ = env.step(a[0])
            # 次のQ値
            Q1 = sess.run(Qout, feed_dict={
                inputs1:np.identity(env.observation_space.n)[s1:s1+1]})
            # 最大のQ値をとりだす
            maxQ1 = np.max(Q1)
            # Q値の計算値をtargetQへ格納
            targetQ = allQ
            # targetQの先頭をベルマン方程式で更新し次のQ値にする
            targetQ[0, a[0]] = r + y * maxQ1
            
            # 重みの更新
            _, W1 = sess.run([updateModel, W], feed_dict={
                inputs1: np.identity(env.observation_space.n)[s:s+1], 
                nextQ:   targetQ})
            # 累積和を計算
            rAll += r
            # 次の状態を現在の状態にして次のループに供える
            s = s1
            # もし穴に落ちていたら
            if d == True:
                # 閾値を更新し、次のエピソードへ
                e = 1.0/((i/500) + 10)
                break
        print(str(i) + " episodes finished")
        # 各エピソードで何回まで進んだか
        jList.append(j)
        # 報酬の累積和リストのさいごに追加
        rList.append(rAll)

print("Suucess Episode Ratio:" + str(sum(rList)/num_episodes) + "%")

# 1:成功、0:失敗
plt.plot(rList)
plt.savefig("success_episodes.png")

# 何回で成功or失敗したか
plt.plot(jList)
plt.savefig("steps_episodes.png")


