# Zenn MCP サーバー

Zennの記事を検索・要約してMarkdownレポートを生成するMCPサーバーです。

## Claude Code開発ルール

### ドキュメント管理

- 開発を進める中でやり方が変わった際は必ず `@CLAUDE.md`、`@docs/` 配下のファイルを更新し、常に最新の状態にする

### 検索・調査

- 作業の中でブラウザ検索をする必要が出た場合は、必ず `gemini-google-search` を用いる
  - 一度でうまく接続できない時があるので、何度か試すこと

### テスト駆動開発

- 開発はテスト駆動で行う。`@docs/tdd_rule.md` に従って開発を行う
- Red → Green → Refactor サイクルを厳守
- 構造変更と振る舞い変更を分離する

### ブランチ・プルリク管理

- ブランチ、プルリクについては `@docs/branch_rule.md` に従う
- ブランチを切って機能開発を行う前に必ず現在の作業状況を確認
- ブランチを切って機能開発を行う前に必ずSOWを作る。SOWは `@docs/sow/` ディレクトリ配下に作成し、機能ごと、バグごとにファイルを作成する
- プルリクエストを出す前に、実装内容をドキュメントにまとめ、 `@docs/dev_log/` フォルダ配下に保存する

### Claude Code Action

- ユーザーへの応答は日本語で行う

### プロジェクトのロギング

- すべてのログには vibelogger ライブラリを使用する
- vibelogger の使用方法: https://github.com/fladdict/vibe-logger/blob/main/README.md
- 問題が発生した際は、`@logs/<project_name>/` フォルダー内のデバッグデータを確認する

### そのほかのルール

- 開発する中で人間の操作が必要な場合は必ず明記して知らせること
  - 例：環境変数の登録など

## 開発内容

`@docs/requirements.md` を参照

- プロジェクト概要・機能要件・非機能要件
- 技術仕様・アーキテクチャ・使用ライブラリ
- インターフェース仕様・MCPツール定義
- 品質要件・セキュリティ・制約事項・リスク分析
- 開発スケジュール・受け入れ基準

## 開発コマンド

- `uv pip install -r requirements.txt` - 依存関係をインストール
- `uv run python app/main.py` - MCPサーバーを起動
- `uv run pytest` - テストを実行

## MCP設定

`@~/.claude/.mcp.json` に追加：

```json
{
  "mcpServers": {
    "zenn-mcp": {
      "command": "uv",
      "args": ["run", "python", "/path/to/zenn_mcp_dev/app/main.py"]
    }
  }
}
```
