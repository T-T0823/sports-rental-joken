# スポーツカー・高級車レンタカー 貸出条件くらべ

スポーツカー・高級車・MT車のレンタカーの「年齢」「免許取得後の年数」の条件を各社横断で比較する非公式ページです。

- 公開ページ: https://t-t0823.github.io/sports-rental-joken/
- 掲載データ: `data.json`（1件＝1プラン。`checked` は確認日、`src` は出典）
- 訂正・追加の連絡: tu.apps.jp@gmail.com

## 広告リンク

data.json の各店に `"aff": "紹介リンクURL"`（任意で `"affLabel"`）を足すと、カードに「PR」付きの予約ボタンが出て、上部に広告表示の告知が自動で出ます。

## 読みもの記事

`guide/` と `sitemap.xml` は `python3 tools/build_guides.py` で data.json から作り直す。data.json を変えたら毎回実行する。
