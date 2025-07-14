# Zenn MCP Server

Zennの記事を検索・要約してMarkdownレポートを生成するMCPサーバーです。

## 概要

このプロジェクトは、Zennの特定トピックに関する記事を取得・要約し、Markdown形式でレポートを生成するMCP（Model Context Protocol）サーバーです。Claude Codeから利用可能で、開発者の情報収集を効率化します。

## 機能

- Zenn記事の検索・取得（いいね数順）
- LLM（Vertex AI Gemini 2.5 Pro）による記事要約
- Markdownレポート生成・保存
- Claude Code統合（3つのMCPツール提供）

## 🚀 初期設定

### 1. 依存関係のインストール

```bash
# uvが未インストールの場合
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
uv sync
```

### 2. Google Cloud Vertex AI セットアップ

詳細は `docs/vertex-ai-setup.md` を参照してください。

#### 方法1: サービスアカウント借用（推奨）

```bash
# Google Cloud CLIでログイン
gcloud auth login

# Application Default Credentials を設定（重要）
gcloud auth application-default login

# プロジェクト設定
gcloud config set project your-gcp-project-id

# Vertex AI API を有効化
gcloud services enable aiplatform.googleapis.com
```

**🔐 認証に関する重要な注意事項**:
- `gcloud auth application-default login` は**初回のみ**実行すれば十分です
- 認証情報は永続的に保存され、自動的にリフレッシュされます
- **Claude Code起動前に毎回実行する必要はありません**
- 長期間使用しない場合（数ヶ月）のみ再認証が必要になることがあります

#### 方法2: サービスアカウントキー（従来方式）

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクト作成
2. Vertex AI API を有効化
3. サービスアカウント作成・キーダウンロード

### 3. 環境変数設定

`.env.example` をコピーして `.env` ファイルを作成：

```bash
# .env.example をコピー
cp .env.example .env

# .env ファイルを編集
# 最低限、GOOGLE_CLOUD_PROJECT を実際のプロジェクトIDに変更
```

#### 方法1使用時（サービスアカウント借用）
```bash
# .env での必須設定
GOOGLE_CLOUD_PROJECT=your-actual-gcp-project-id
```

#### 方法2使用時（サービスアカウントキー）
```bash
# .env での必須設定
GOOGLE_CLOUD_PROJECT=your-actual-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

**重要**: 
- `.env` ファイルはGitで管理されません
- `.env.example` には実際の値を記載しないでください
- 最低限 `GOOGLE_CLOUD_PROJECT` は実際の値に変更が必要です

### 4. Claude Code MCP設定

`~/.claude/.mcp.json` に以下を追加：

```json
{
  "mcpServers": {
    "zenn-mcp": {
      "command": "uv",
      "args": ["run", "python", "/Users/hayashiyusuke/Desktop/self_learning/mcp/zenn_mcp_dev/app/main.py"]
    }
  }
}
```

**注意**: `args` の配列内のパスを、実際のプロジェクトディレクトリのパスに変更してください。

### 5. 動作確認

```bash
# 設定テスト
uv run python -c "
from app.vertex_ai_client import VertexAIClient
client = VertexAIClient()
print('Vertex AI接続テスト:', 'OK' if client.test_connection() else 'NG')
"

# MCPサーバー起動テスト
uv run python app/main.py
```

MCPサーバーが正常に起動すれば、Claude Codeから以下のツールが利用可能になります：
- `search_zenn_articles`: 記事検索・要約・レポート生成
- `get_article_summary`: 個別記事要約
- `save_report`: レポート保存

## 🎯 使用方法

### Claude Codeでの使用例

初期セットアップ完了後は、Claude Codeを普通に起動するだけで利用可能です。

```
Reactについて最新の記事を調べて要約してください
```

Claude Codeが自動的に `search_zenn_articles` ツールを使用して：
1. Zennから「React」トピックの最新記事を取得
2. 各記事を要約
3. Markdownレポートを生成

**注意**: サービスアカウント借用を使用している場合、特別な認証手順は不要です。

### 直接実行（開発・テスト用）

```bash
# MCPサーバー起動
uv run python app/main.py

# テスト実行
uv run pytest

# 統合テスト
uv run pytest tests/test_integration.py -v
```

## 📁 プロジェクト構成

```
zenn_mcp_dev/
├── app/                    # メインアプリケーション
│   ├── main.py            # MCP エントリーポイント
│   ├── crawler.py         # Zenn記事取得
│   ├── summarizer.py      # 統合要約機能
│   ├── renderer.py        # Markdown生成
│   ├── vertex_ai_client.py # Vertex AI クライアント
│   └── config.py          # 設定管理
├── tests/                 # テストコード
├── docs/                  # ドキュメント
│   ├── vertex-ai-setup.md # Vertex AI設定詳細
│   └── github-actions-setup.md # CI/CD設定
├── logs/                  # ログファイル
├── .env                   # 環境変数（要作成）
├── CLAUDE.md             # 開発ルール
└── README.md             # このファイル
```

## 🔧 トラブルシューティング

### よくある問題

| 問題 | 解決方法 |
|------|----------|
| `ModuleNotFoundError` | `uv sync` で依存関係を再インストール |
| `DefaultCredentialsError` | `gcloud auth application-default login` を実行、または `.env` ファイルの `GOOGLE_APPLICATION_CREDENTIALS` パスを確認 |
| `403 Forbidden` | Vertex AI API が有効化されているか確認 |
| `Cloud project not found` | `gcloud config set project your-project-id` でプロジェクト設定を確認 |
| Claude Codeでツールが見つからない | `~/.claude/.mcp.json` のパス設定を確認 |

### 認証関連のトラブルシューティング

#### サービスアカウント借用使用時
```bash
# 現在の認証状態を確認
gcloud auth list

# Application Default Credentialsの確認
gcloud auth application-default print-access-token

# 認証エラーが発生した場合のリセット・再設定
gcloud auth application-default revoke
gcloud auth application-default login
```

#### 認証の仕組み
- **初回設定後は自動継続**: 認証情報は `~/.config/gcloud/application_default_credentials.json` に保存
- **自動リフレッシュ**: トークンの期限切れ時も自動的に更新
- **再認証が必要な場合**: 長期間（数ヶ月）使用しない場合のみ

### ログ確認

```bash
# アプリケーションログ
tail -f logs/zenn_mcp/zenn_mcp.log

# MCPサーバーのデバッグ出力
PYTHONPATH=. uv run python app/main.py --debug
```

## 📖 詳細ドキュメント

- [`CLAUDE.md`](CLAUDE.md): 開発ルール・コマンド
- [`docs/requirements.md`](docs/requirements.md): 要件定義・技術仕様
- [`docs/vertex-ai-setup.md`](docs/vertex-ai-setup.md): Vertex AI設定詳細
- [`docs/github-actions-setup.md`](docs/github-actions-setup.md): CI/CD設定

## 📄 ライセンス

MIT License

---

**開発者向け**: 開発は日本語で行い、テスト駆動開発を採用しています。詳細は `CLAUDE.md` を参照してください。