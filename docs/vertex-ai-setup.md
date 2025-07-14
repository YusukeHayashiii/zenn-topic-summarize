# Vertex AI セットアップガイド

Zenn MCP サーバーでVertex AI（Gemini）を使用するためのセットアップ手順です。

## 🔧 Google Cloud セットアップ

### 1. プロジェクト作成・API有効化

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクト作成
2. 以下のAPIを有効化：
   - Vertex AI API
   - Compute Engine API

### 2. 環境変数設定

`.env` ファイルを作成：

```bash
# .env
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
VERTEX_AI_LOCATION=us-central1
VERTEX_AI_MODEL=gemini-2.5-pro
```

### 3. 利用可能なモデル

| モデル名 | 説明 | 推奨用途 |
|---------|------|---------| 
| `gemini-2.5-pro` | 高性能な汎用モデル | 複雑な要約・分析 |
| `gemini-2.5-flash` | コストが安い | 簡単な要約 |

## 🚀 使用方法

```python
from app.vertex_ai_client import VertexAIClient

# クライアント初期化
client = VertexAIClient()

# テキスト要約
summary = client.summarize_text("長い記事の内容...", max_length=300)

# 接続テスト
if client.test_connection():
    print("Vertex AI への接続が成功しました")
```

## 🧪 テスト実行

```bash
# 設定テスト
uv run pytest tests/test_config.py::test_vertex_ai_config_defaults -v

# Vertex AI クライアントテスト
uv run pytest tests/test_vertex_ai.py -v

# 接続テスト
uv run python -c "
from app.vertex_ai_client import VertexAIClient
client = VertexAIClient()
print('接続テスト結果:', 'OK' if client.test_connection() else 'NG')
"
```

## 🔍 トラブルシューティング

### よくある問題

| エラー | 解決方法 |
|--------|----------|
| `DefaultCredentialsError` | `GOOGLE_APPLICATION_CREDENTIALS` 環境変数を確認 |
| `403 Forbidden` | Vertex AI API有効化とサービスアカウント権限を確認 |
| `Location not supported` | `VERTEX_AI_LOCATION` を利用可能な地域に変更 |
| `Model not found` | モデル名と利用可能地域を確認 |


## 📋 設定チェックリスト

- [ ] Google Cloud プロジェクト作成済み
- [ ] Vertex AI API 有効化済み
- [ ] サービスアカウント作成・権限設定済み
- [ ] 環境変数設定済み
- [ ] 接続テスト成功