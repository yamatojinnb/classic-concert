# classic-concert

クラシックコンサート情報をコンサートスクウェアから取得し、GitHub Pagesで横断検索サイトとして公開するプロジェクト。

## 構成
| ファイル | 役割 |
|---|---|
| `scraper.py` | コンサートスクウェアを巡回し `concerts.json` を出力 |
| `build.py` | `concerts.json` から `index.html`（検索サイト）を生成 |
| `index.html` | 公開する静的サイト（リポジトリ直下＝Pagesのルート公開用） |
| `.github/workflows/update.yml` | 日次で scrape→build→mainブランチへコミット |

## ローカル実行
```bash
pip install -r requirements.txt
python scraper.py --max 2   # 動作確認（先頭2ページ）
python build.py             # index.html を生成
```
`index.html` をブラウザで開けば動作確認できます。

## GitHub Pages 公開手順（main ブランチ / ルート）
1. リポジトリの **Settings → Pages** を開く
2. **Build and deployment → Source** で **「Deploy from a branch」** を選択
3. **Branch** を **`main`** ／ フォルダを **`/ (root)`** に設定して **Save**
4. 数十秒〜数分後、同じ画面に表示されるURL（`https://<ユーザー名>.github.io/classic-concert/`）で公開サイトを確認

## 自動更新の仕組み
`update.yml` が毎日06:00 JSTに実行され、`scraper.py` → `build.py` で `index.html` と `concerts.json` を再生成し、**mainブランチに直接コミット＆push**する。ブランチ公開方式のため、Pages側の追加設定は不要（pushされた最新の`index.html`が自動的に反映される）。

## 注意
- スクレイピングは礼儀としてアクセス間隔1秒。負荷配慮のためCIは先頭20ページに制限（`--max 20`）。全件にするなら workflow から `--max` を外す。
- 各サイトの利用規約を遵守し、AI学習用途への転用はしない。
- 曲目はコンサートスクウェア上で独立フィールドが無く、説明本文に含まれる場合のみ取得。
- 初回データは一覧情報のみ（出演者・料金の詳細取得は未実施）。詳細を含めるには `python scraper.py`（`--max`なし・所要時間長め）を実行して再生成する。
