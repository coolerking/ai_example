# coding: utf-8
'''青空文庫データをつかってLSTMモデルを学習させ
テキストを生成するサンプルプログラム

(C) Tasuku Hori, exa Corporation Japan, 2017. all rights reserved.
'''

__author__ = 'Tasuku Hori'

from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file

import numpy as np
import random
import codecs
import sys

clean_pathList = ['bocchan.txt.clean.txt',
            'kazeno_matasaburo.txt.clean.txt',
            'ningen_shikkaku.txt.clean.txt',
            'rashomon.txt.clean.txt',
            'wagahaiwa_nekodearu.txt.clean.txt']



def main():
    '''メイン関数
    clean_pathListの各データごと学習させ、結果を標準出力へ表示する。
    '''

    for clean_path in clean_pathList:
        print("Wrote model file: " + text_generator(clean_path))


def text_generator(clean_path):
    '''引数で渡されたファイル名の内容を学習データとしてバッチを実行し、
    イテレーションごとに予測した文書サンプルを表示する。
    '''
    with codecs.open(clean_path + ".log", "w", "utf-8") as f:
        f.write("=" * 50)
        f.write("\n")
        f.write("Path: " + clean_path +"\n")
        
        bindata = open(clean_path, 'rb').read()
        text = bindata.decode('utf-8')
        
        f.write("Size of text: " + str(len(text)) + "\n")

        chars = sorted(list(set(text)))

        f.write("Total chars: " + str(len(chars)) + "\n")

        # 正引き逆引き辞書
        char_indices = dict((c,i) for i,c in enumerate(chars))
        indices_char = dict((i,c) for i,c in enumerate(chars))

        # 切り取る文字数
        maxlen = 40
        # step 次何文字前にするか
        step = 3
        # 切り出した文字列
        sentences = []
        # 次に来る文字
        next_chars = []

        f.write("maxlen: " + str(maxlen) + "\n")
        f.write("step:   " + str(step) + "\n")
        
        for i in range(0, len(text) - maxlen, step):
            sentences.append(text[i:i + maxlen])
            next_chars.append(text[i + maxlen])

        f.write("Number of sentences: " + str(len(sentences)) + "\n")

        # テキストのベクトル化
        X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
        y = np.zeros((len(sentences), len(chars)), dtype=np.bool)

        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                X[i, t, char_indices[char]] = 1
            y[i, char_indices[next_chars[i]]] = 1

        # モデルを定義する

        model = Sequential()
        # セル数=128
        cell = 128
        f.write("cell:   " + str(cell) + "\n")
        model.add(LSTM(cell, input_shape=(maxlen, len(chars))))
        model.add(Dense(len(chars)))
        model.add(Activation('softmax'))

        # lr:学習レート=0.01
        learn_rate = 0.01
        f.write("lean rate: " + str(learn_rate) + "\n")
        optimizer = RMSprop(lr=learn_rate)

        # モデルのコンパイル
        # 損失関数を指定
        model.compile(loss='categorical_crossentropy', optimizer=optimizer)

        # 
        def sample(preds, temperature=1.0):
            preds = np.asarray(preds).astype('float64')
            preds = np.log(preds) / temperature
            exp_preds = np.exp(preds)
            preds = exp_preds / np.sum(exp_preds)
            probas = np.random.multinomial(1, preds, 1)
            # 配列の中で最も大きな値の位置を返す
            return np.argmax(probas)

        count = 100
        for iteration in range(1, count):
            f.write("\n")
            f.write("-" * 50)
            f.write("\n")
            f.write("iteration: " + str(iteration) + "/" + str(count) +"\n")

            model.fit(X, y, batch_size=128, epochs=1)

            start_index = random.randint(0, len(text) - maxlen -1)

            # サンプルを出力するデータを以下の４つの中から１つ選ぶ
            for diversity in [0.2, 0.5, 1.0, 1.2]:
                f.write("\n")
                f.write("----- diversity " + str(diversity) + "\n")

                generated = ''
                sentence = text[start_index: start_index + maxlen]
                generated += sentence
                f.write("----- Seed generated '" + sentence +"'\n")
                f.write("\n")
                f.write("'" + generated + "' ")
    
                # 次の文字を予測して順番に足していく
                for i in range(400):
                    x = np.zeros((1, maxlen, len(chars)))
                    for t, char in enumerate(sentence):
                        x[0, t, char_indices[char]] = 1.
        
                    # 次の文字を予測
                    preds = model.predict(x, verbose=9)[0]
                    next_index = sample(preds, diversity)
                    next_char = indices_char[next_index]
        
                    generated += next_char
                    sentence = sentence[1:] + next_char
        
                    f.write(next_char)
                    f.flush()
                f.write("\n")

        # モデルの保存
        model.save("textgen_model_"+ clean_path +".h5")
        return "textgen_model_"+ clean_path + ".h5"


if __name__ == "__main__":
    '''コマンドラインからモジュール実行された場合、main()を実行する。
    '''
    try:
        main()
        print()
        print('Completed')
    except Exception as e:
        print(e)

