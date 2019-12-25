
# 「みんなのディープラーニング講座 ゼロからChainerとPythonで学ぶ深層学習の基礎」コード集

本リポジトリは [表題のUdemy講座](https://www.udemy.com/deep-learning/learn/v4/overview) 内で実際に作成したコードをまとめたものです。

## 実行環境

講座ではPyCharmを使っていましたが、私は以下の環境でJupyter notebooks を起動して実行していました。

- Windows 7
- Anaconda3 5.0.1
 - conda "opencv" にて以下のパッケージを関連パッケージ含めてインストール
  - scikit-learn
  - matplotlib
  - numpy
  - chainer
 - すべてjupyter notebook をlaunchして実行

なお、最終章のCNNの学習は約30分かかりました(ThinkPad X230、GPUなし)。

## Jupyter notebooks

|セクション|レクチャ|ファイル名|
|:--------|:------|:--------|
| 6. Chainerの基礎| 49. プロジェクトの立ち上げとChainerのインストールの確認～ | 01_Variable.ipynb |
| 6. Chainerの基礎| 51. Links                                             | 02_Links.ipynb |
| 6. Chainerの基礎| 53. Functions                                         | 03_Functions.ipynb |
| 6. Chainerの基礎| 52. Chain                                             | 04_Chain.ipynb |
| 6. Chainerの基礎| 54. Optimizer                                         | 05_Optimizer.ipynb |
| 6. Chainerの基礎|  55. ChainerのHello World                             | 06_Chainer_hello_world.ipynb |
| 7. ディープラーニングによる分類 | 56. ディープラーニングによる分類の概要～   | 11_Iris_Datasets.ipynb |
| 7. ディープラーニングによる分類 | 58. Irisのデータ処理                     | 12_Iris_data_processing.ipynb |
| 7. ディープラーニングによる分類 | 60. Irisの分類                          | 13_Iris_Classification.ipynb |
| 7. ディープラーニングによる分類 | 61. Trainerによる訓練                    | 13_Iris_Trainer.ipynb |
| 7. ディープラーニングによる分類 | 62. Serializerによるモデルの保存          | 15_Iris_Serializer.ipynb |
| 7. ディープラーニングによる分類 | 62. Serializerによるモデルの保存          | 16_Iris_Serializer_load.ipynb |
| 8. 畳み込みニューラルネットワーク | 63. 畳み込みニューラルネットワークの概要～ | 21_CNN_MNIST.ipynb |
| 8. 畳み込みニューラルネットワーク | 66. 畳み込みニューラルネットワークの学習 | 22_CNN_train.ipynb |
| 8. 畳み込みニューラルネットワーク | 67. 畳み込みニューラルネットワークによる分類 | 23_CNN_test.ipynb |
