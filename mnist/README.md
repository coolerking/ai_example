# Deep MNIST for Experts サンプルコード

## `mnist_expert.py`

TensorFlow チュートリアルの"Deep MNIST for Expoerts"に記述されているコードを集約したものです。

```bash
python mnist_expert.py
```

で実行可能です。

詳細は [チュートリアル](https://www.tensorflow.org/get_started/mnist/pros) を参照してください。

## Floyd Hub

[Floyd Hub](https://www.floydhub.com/) でも実行可能です。

Floyd Hub アカウントを取得してログインし、クライアントPC上のPython実行環境上で `pip install floyd` してから、Floyd Hubコンソール上で"mnist"という名前でプロジェクトを新規起動して、以下の操作を行ってください。


```bash
(C:\.. Anaconda3) C:\ ..ai_samples> cd mnist
(C:\.. Anaconda3) C:\ ..mnist> floyd login
※ブラウザが上がるのでそこのセキュリティコードをペーストしてEnter

(C:\.. Anaconda3) C:\ ..mnist> floyd init mnist
(C:\.. Anaconda3) C:\ ..mnist> floyd run --cpu --env tensorflow-1.3 "python mnist_expert.py"
```

## 実行時間目安

|CPU|メモリ|GPU|OS|Python|TensorFlow|所要時間|備考|
|:--|-----:|:-:|:-|:----:|:--------:|:------:|:---|
|i5 2.6GHz(4コア)|8GB|N/A|Windows7Pro|Anaconda3(4.4.0:py3.6.0)|1.4.0|1時間18分20秒|占有ではなく、裏で別のプロセスも上がっていた|
|i7 2.2GHz(8コア)上のコンテナ|16GB|GTX1050Ti|Ubuntu16.04LTS|Python3.5.2|tensorflow/tensorflow:1.3.0-gpu-py3|約3分|Jupyter Nodebook上で実行、腕時計計測|
|i7 2.2GHz(8コア)上のコンテナ|16GB|N/A|Ubuntu16.04LTS|Python3.5.2|tensorflow/tensorflow:1.3.0-py3|38分31秒|別コンテナ1個動作中の状態|
|Floyd Hub CPUのみ|不明|N/A|不明|Python3|1.3.0|53分11秒|無料枠内で完遂可能|
