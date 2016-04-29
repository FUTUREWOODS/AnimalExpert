############実行ファイル####################
watson5P.py
  ....watsonで音声認識し、かつその内容をPepperに喋らせ、またPepperのマイクをストリーミングして流す
watson5G.py
  ...watsonで音声認識のみ
watson5Q.py
  ...watsonで音声認識を行い、かつ単語が「チーズ」であれば、写真を撮って保存する。opencvが必要。



##########以下、依存ファイル達###############
watsonStream.py
 ...watsonの本体。リアルタイムに認識させる為にrun()でまずwebsocketを開く。
    後はsend()で音声データを送ると、_on_message()にJson型で帰ってくるので平文に変換してフラグを立てる.

watsonC.py
 ...watsonを包み込むモジュール。重要なのはrecognize_stream()だけで他はtokenとかurlの変換をやってるだけのクラス。

PepperStream.py
 ...Pepperを喋らせたり、マイクのストリームを行うクラス