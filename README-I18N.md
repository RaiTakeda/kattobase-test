# KATTOBASE 多言語化の基盤（試作）

現在の公開サイトであるルートの `index.html` は**変更しません**。

## 構成

- `src/index.html`: 現行ページをコピーした共通HTMLテンプレート。トップの紹介文とページメタ情報のみ `{{hero.title}}` のようなキーに置き換えています。
- `locales/en.json`: 英語（基準言語）
- `locales/ja.json`: 日本語
- `locales/zh-TW.json`: 台湾華語（繁体字）
- `locales/ko.json`: 韓国語
- `scripts/build.py`: Python標準ライブラリだけで各言語版HTMLを生成します。

## プレビューの生成

リポジトリのルートで以下を実行します。

```bash
python scripts/build.py
```

生成先：

```text
_build/
  en/index.html
  ja/index.html
  zh-TW/index.html
  ko/index.html
```

ローカルで確認する場合：

```bash
python -m http.server 8000
```

ブラウザで `http://localhost:8000/_build/en/` などを開きます。プレビュー用の相対画像パスはリポジトリのルートを参照します。

## 現段階の制限（重要）

- **実際に翻訳済みなのはトップページの紹介文とHTMLのタイトル・説明のみです。** 観戦ガイドの本文、ヘッダー、サイドメニュー、JavaScript生成文言、図内の日本語は未翻訳です。
- 生成物には `noindex, nofollow` を含めています。**未翻訳ページをそのまま一般公開・検索登録しないでください。**
- 現在の言語切り替えUIはまだ生成ページに接続していません。
- ビルド時に日本語の既存HTMLとテンプレートが自動同期する仕組みは未実装です。今後は `src/index.html` を唯一の編集元にし、検証後に公開用各言語HTMLを生成する運用に移行します。
- URL `/en/`, `/ja/`, `/zh-tw/`, `/ko/` や `hreflang` の正式設定は全体翻訳と公開準備の段階で行います。

## 翻訳を追加する手順

1. `src/index.html` の翻訳したい文字列を `{{guide.step1.title}}` のようなキーへ変更
2. 4つの `locales/*.json` に同名のキーを追加
3. `python scripts/build.py` で欠落キーと出力を確認
4. 翻訳の確認後に公開側へ反映

`src/index.html` は現時点でのスナップショットです。公開中の `index.html` を変更した場合は、テンプレート側にも変更内容を反映してください。
