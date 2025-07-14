# Zenn MCP サーバー

Zennの記事を検索・要約してMarkdownレポートを生成するMCPサーバーです。

## Claude Code開発ルール

開発は全て日本語で行う。

### ドキュメント管理

- 開発を進める中でやり方が変わった際は必ず `@CLAUDE.md`、`@docs/` 配下のファイルを更新し、常に最新の状態にする

### 検索・調査

- 作業の中でブラウザ検索をする必要が出た場合は、必ず `gemini-google-search` を用いる
  - 一度でうまく接続できない時があるので、何度か試すこと

#### 補足：`gemini-google-search` について

この開発環境で使用しているmcpサーバーであり、`@~/.claude/.mcp.json` に追加して使用している。

```json
{
  "mcpServers": {
    "gemini-google-search": {
        "command": "npx",
        "args": ["mcp-gemini-google-search"],
        "env": {
          "GEMINI_PROVIDER": "vertex",
          "VERTEX_PROJECT_ID": "your-gcp-project-id",
          "VERTEX_LOCATION": "us-central1",
          "GEMINI_MODEL": "gemini-2.5-flash"
        }
      }
  }
}
```

### テスト駆動開発

- 開発はテスト駆動で行う。`@docs/tdd_rule.md` に従って開発を行う
- Red → Green → Refactor サイクルを厳守
- 構造変更と振る舞い変更を分離する

### ブランチ・プルリク管理

- ブランチ、プルリクについては `@docs/branch_rule.md` に従う
- ブランチを切って機能開発を行う前に必ず現在の作業状況を確認
- ブランチを切って機能開発を行う前に必ずSOWを作る。SOWは `@docs/sow/` ディレクトリ配下に作成し、機能ごと、バグごとにファイルを作成する
- プルリクエストを出す前に、実装内容をドキュメントにまとめ、 `@docs/dev_log/` フォルダ配下に保存する
- **プルリクエスト作成前に必須**: 以下のドキュメント更新プロセスを実行する
  1. `@docs/requirements.md` のディレクトリ構成・進捗状況を最新に更新
  2. 他の関連ドキュメント (`@docs/` 配下) の内容を調査し、更新が必要な箇所を反映
  3. 実装した機能に関連する設定・技術仕様の変更を各ドキュメントに反映

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

以下の設定を`.mcp.json`に追加する。
詳細は[公式ページ](https://docs.anthropic.com/ja/docs/claude-code/settings#%E8%A8%AD%E5%AE%9A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB)を参照

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
