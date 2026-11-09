# KATTOBASE 多言語化の基盤（公開プレビュー）

現在の公開サイトであるルートの `index.html` は**変更しません**。

## 構成

- `src/index.html`: 現行ページをコピーした共通HTMLテンプレート。トップの紹介文とページメタ情報のみ `{{hero.title}}` のようなキーに置き換えています。
- `locales/en.json`: 英語（基準言語）
- `locales/ja.json`: 日本語
- `locales/zh-TW.json`: 台湾華語（繁体字）
- `locales/ko.json`: 韓国語
- `scripts/build.py`: Python標準ライブラリだけで各言語版HTMLを生成します。

## GitHub Pages上のプレビュー

GitHub Pages上に、検索登録を抑制したテスト用ページを配置しています。

- 入口: https://raitakeda.github.io/kattobase-test/preview/
- 英語: https://raitakeda.github.io/kattobase-test/preview/en/
- 日本語: https://raitakeda.github.io/kattobase-test/preview/ja/
- 台湾華語: https://raitakeda.github.io/kattobase-test/preview/zh-TW/
- 韓国語: https://raitakeda.github.io/kattobase-test/preview/ko/

`.github/workflows/build-preview.yml` によって `src/**`、`locales/**`、`scripts/build.py` またはワークフロー本体を更新すると、`python scripts/build.py --output preview` が実行され、生成物が `main` ブランチの `preview/` へ自動コミットされます。`workflow_dispatch` による手動実行も可能です。GitHub Pagesがブランチのルートから公開している構成を利用します。

**プレビューURLは誰でも閲覧できます。** `noindex, nofollow` は検索登録の抑止であり、アクセス制限ではありません。公開用の `index.html` は変更されません。

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
  index.html        ← 保存された言語へ移動する入口
```

ローカルで確認する場合：

```bash
python -m http.server 8000
```

ブラウザで `http://localhost:8000/_build/` を開きます。初回は英語版に移動します。`http://localhost:8000/_build/en/` 等を直接開くこともできます。プレビュー用の相対画像パスはリポジトリのルートを参照します。

## 現段階の制限（重要）

- **実際に翻訳済みなのはトップページの紹介文とHTMLのタイトル・説明のみです。** 観戦ガイドの本文、ヘッダー、サイドメニュー、JavaScript生成文言、図内の日本語は未翻訳です。
- 生成物には `noindex, nofollow` を含めています。ローカル生成先 `_build/` は `.gitignore` でGitへの追加を抑制します。一方、GitHub Actionsが生成する `preview/` は一般閲覧可能なテストページとして公開します。**未翻訳ページをそのまま一般公開・検索登録しないでください。**
- **ローカルプレビューの言語切り替えは実装済みです。** 各言語URLは `_build/<言語>/` で、切り替え時は `#city` などのページ内位置を保持し、選択言語を `localStorage` の `kattobase.preferredLanguage` に保存します。次回 `_build/` にアクセスすると、保存された言語に移動します。各言語URLを直接指定した場合は、その指定が優先されます。
- 翻訳未完了のため、**現在公開中のルート `index.html` の言語ボタンは変更していません。**
- ビルド時に日本語の既存HTMLとテンプレートが自動同期する仕組みは未実装です。今後は `src/index.html` を唯一の編集元にし、検証後に公開用各言語HTMLを生成する運用に移行します。
- URL `/en/`, `/ja/`, `/zh-tw/`, `/ko/` や `hreflang` の正式設定は全体翻訳と公開準備の段階で行います。

## 翻訳を追加する手順

1. `src/index.html` の翻訳したい文字列を `{{guide.step1.title}}` のようなキーへ変更
2. 4つの `locales/*.json` に同名のキーを追加
3. `python scripts/build.py` で欠落キーと出力を確認
4. 翻訳の確認後に公開側へ反映

`src/index.html` は現時点でのスナップショットです。公開中の `index.html` を変更した場合は、テンプレート側にも変更内容を反映してください。

## 言語切り替えの確認手順

1. `python scripts/build.py` でプレビューを再生成。
2. `python -m http.server 8000` でローカルサーバーを起動。
3. `http://localhost:8000/_build/en/#tickets` を開き、日本語に切り替えると `/ja/#tickets` に移ることを確認。
4. 言語メニューに選択中の言語が表示され、チェックマークが付くことを確認。
5. `http://localhost:8000/_build/` を新たに開き、最後に選んだ言語が開くことを確認。
6. `http://localhost:8000/_build/ko/` のような明示URLを開いた場合は、保存言語に関係なく指定言語で開くことを確認。
7. `http://localhost:8000/` の公開版に対応する既存 `index.html` が変更されていないことを確認。

注意：プレビューの全ページが翻訳完了したわけではありません。未翻訳部分を含むため正式公開や検索登録には使用しないでください。
