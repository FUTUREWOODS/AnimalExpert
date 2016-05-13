# BingCrawling(推奨)
Bing search APIを叩く
- Bing search APIを叩く為には，Microsoft Azure Marketplaceのアカウントを作成し，プライマリアカウントキーを取得する必要がある
	
## 実行ファイル
### /BingCrawling/getPic/getPic.py
キーワードに関する画像をBingから取得するプログラム
- /BingCrawling/getPic/以下に検索したキーワード名のフォルダが作成され，その中に画像が保存される
- 取得画像枚数はデフォルトは3枚(変更可)	

### /BingCrawling/getUrlAndTitle/
キーワードに関するwebページのURLとタイトルを取得するプログラム
- json形式で出力

# PyCherryPick(非推奨)
コマンドライン引数として与えられたURLより下位層のページを探索し，引数として与えられた拡張子のファイルを取得する
- Wikipediaとgoogle画像検索からはファイルを取得することができない(Wikipwdiaからファイルを取得するためには専用のAPIが必要かも)

##実行ファイル
/PyCherryPick/python/pycherrypick.py
## 実行方法
python pycherrypick.py <検索するURL>　-t <検索するファイルの形式(ex. jpg, png, pdf, etc..)>

# TODO
- アプリ初回起動時に，Pepper管理者のMicrosoft Azure Marketplaceアカウントのプライマリアカウントキーをタブレットから入力してもらう仕組みを作る必要がある
	- 今はソースコード中に直接埋め込んでいるが，リリースする際には改良を加える必要があると思う
