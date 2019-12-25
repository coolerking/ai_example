# 【Pythonで学ぶ】OpenCVでの画像処理入門

## 前提

- Windows 7 Professional
- Anaconda3 5.0.1
 - python3.5.x ベースのconda環境"opencv"を構築
  - conda install opencv3
  - conda install matplotlib
 - jupyter notebooks をlaunch

OpenCVの `imshow()` を使って別画面表示させるサンプルコードは、Dockerコンテナ起動のJupyter notebooks では動作しません。

## サンプルコード

|概要                      |Jupyter notebooks ファイル |
|:-------------------------|:--------------------------|
|2値化(白黒化)             | [binary_black_white](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/binary_black_white.ipynb) |
|2値化＋トラックバー       | [binary_track_bar](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/binary_track_bar.ipynb) |
|アファイン変換            | [afine.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/afine.ipynb) |
|インペイント              | [inpaint.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/inpaint.ipynb) |
|ウィンドウの調整          | [window_resize.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/window_resize.ipynb)
|エッジの検出(Canny)       | [edge_canny.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/edge_canny.ipynb) |
|オプティカルフロー        | [optical_flow.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/optical_flow.ipynb) |
|ガンマ変換                | [ganma.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/ganma.ipynb) |
|トラックバーの作成        | [track_bar.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/track_bar.ipynb) |
|パーティクルフィルタ      | [particle_filter.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/particle_filter.ipynb) |
|ヒストグラム              | [histgram.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/histgram.ipynb) |
|ヒストグラム均一化        | [histgram_equalize.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/histgram_equalize.ipynb) |
|ブロブの検出              | [blob.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/blob.ipynb) |
|マウスイベント            | [mouse_event.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/mouse_event.ipynb) |
|モルフォロジー演算        | [morphology.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/morphology.ipynb) |
|リサイズ                  | [resize.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/resize.ipynb) |
|動画の表示・出力          | [movie.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/movie.ipynb) |
|図形の描画                | [draw.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/draw.ipynb) |
|特徴抽出                  | [feature.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/feature.ipynb) |
|画像の平滑化              | [smoothing.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/smoothing.ipynb) |
|画像の微分・エッジの検出  | [edge_differential.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/edge_fifferential.ipynb) |
|画像の表示・出力          | [imshow.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/imshow.ipynb) |
|畳み込みの基礎            | [conv.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/conv.ipynb) |
|直線・円の検出            | [line_circle.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/line_circle.ipynb) |
|背景差分                  | [back.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/back.ipynb) |
|色検出                    | [color.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/color.ipynb) |
|色空間・グレースケール    | [color_space.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/color_space.ipynb) |
|輪郭の検出                | [figure_edge.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/figre_edge.ipynb) |
|透視変換                  | [perspective.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/perspective.ipynb) |
|顔検出                    | [face.ipynb](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/face.ipynb) |


## データ

- [data,zip](http://pandagit.exa-corp.co.jp/89004/ai_samples/tree/master/udemy/opencv/data.zip)~
本講座で扱う全てのデータを圧縮したファイル。最初に展開しておく。


