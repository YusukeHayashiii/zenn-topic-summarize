# Vertex AI セットアップガイド

このドキュメントでは、Zenn MCP サーバーでVertex AI（Gemini）を使用するためのセットアップ手順を説明します。

## 🔧 Google Cloud Platform セットアップ

### 1. Google Cloud プロジェクトの作成・設定

#### プロジェクトの作成
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成または既存プロジェクトを選択
3. プロジェクトIDをメモしておく（例: `my-zenn-mcp-project`）

#### 必要なAPIの有効化
```bash
# Google Cloud CLI を使用する場合
gcloud services enable aiplatform.googleapis.com
gcloud services enable compute.googleapis.com
```

または、Google Cloud Console で以下を手動で有効化：
- Vertex AI API
- Compute Engine API

### 2. 認証設定

#### サービスアカウントの作成
1. Google Cloud Console で「IAM & Admin」→「Service Accounts」に移動
2. 「CREATE SERVICE ACCOUNT」をクリック
3. サービスアカウント情報を入力：
   - **Name**: `zenn-mcp-vertex-ai`
   - **Description**: `Zenn MCP Server Vertex AI access`
4. 必要な権限を付与：
   - `Vertex AI User`
   - `AI Platform Developer` (optional, for additional features)
5. JSON キーファイルをダウンロード

#### 認証方法

**方法1: サービスアカウントキー（推奨）**
```bash
# キーファイルのパスを環境変数に設定
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

**方法2: gcloud CLI認証**
```bash
# Google Cloud CLIでログイン
gcloud auth login
gcloud config set project your-project-id
gcloud auth application-default login
```

## 🛠️ アプリケーション設定

### 1. 環境変数設定

以下の環境変数を設定します：

```bash
# 必須設定
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"

# オプション設定（デフォルト値あり）
export VERTEX_AI_LOCATION="us-central1"  # デフォルト: us-central1
export VERTEX_AI_MODEL="gemini-1.5-pro"  # デフォルト: gemini-1.5-pro
```

### 2. .env ファイル作成

プロジェクトルートに `.env` ファイルを作成：

```bash
# .env
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
VERTEX_AI_LOCATION=us-central1
VERTEX_AI_MODEL=gemini-1.5-pro
```

**注意**: `.env` ファイルは `.gitignore` に含まれているため、リポジトリにコミットされません。

### 3. 利用可能なモデル

Vertex AI で利用可能な Gemini モデル：

| モデル名 | 説明 | 推奨用途 |
|---------|------|---------|
| `gemini-1.5-pro` | 高性能な汎用モデル | 複雑な要約・分析 |
| `gemini-1.5-flash` | 高速レスポンス | 簡単な要約 |
| `gemini-1.0-pro` | 安定版 | 一般的な用途 |

## 🚀 使用方法

### 1. 基本的な使用例

```python
from app.vertex_ai_client import VertexAIClient

# クライアント初期化
client = VertexAIClient()

# テキスト要約
summary = client.summarize_text("長い記事の内容...", max_length=300)
print(summary)

# 接続テスト
if client.test_connection():
    print("Vertex AI への接続が成功しました")
else:
    print("接続に失敗しました")
```

### 2. 複数テキストの並列要約

```python
texts = ["記事1の内容", "記事2の内容", "記事3の内容"]
summaries = client.summarize_multiple_texts(texts, max_length=250)

for i, summary in enumerate(summaries):
    print(f"記事{i+1}の要約: {summary}")
```

## 🧪 テスト実行

### 1. 設定テスト
```bash
# 設定テスト実行
uv run pytest tests/test_config.py::test_vertex_ai_config_defaults -v
```

### 2. Vertex AI クライアントテスト
```bash
# Vertex AI クライアントテスト実行
uv run pytest tests/test_vertex_ai.py -v
```

### 3. 統合テスト（要認証設定）
```bash
# 実際のVertex AI を使用したテスト（認証情報必要）
uv run python -c "
from app.vertex_ai_client import VertexAIClient
client = VertexAIClient()
result = client.test_connection()
print('接続テスト結果:', 'OK' if result else 'NG')
"
```

## 🔍 トラブルシューティング

### よくある問題と解決方法

#### 1. 認証エラー
**エラー**: `google.auth.exceptions.DefaultCredentialsError`

**解決方法**:
- `GOOGLE_APPLICATION_CREDENTIALS` 環境変数が正しく設定されているか確認
- サービスアカウントキーファイルが存在し、読み取り可能か確認
- ファイルパスに空白や特殊文字が含まれていないか確認

#### 2. APIアクセスエラー
**エラー**: `403 Forbidden` または `API not enabled`

**解決方法**:
- Vertex AI API が有効になっているか確認
- サービスアカウントに適切な権限があるか確認
- プロジェクトIDが正しく設定されているか確認

#### 3. 地域エラー
**エラー**: `Location not supported`

**解決方法**:
- `VERTEX_AI_LOCATION` を利用可能な地域に変更
- 利用可能地域: `us-central1`, `us-east1`, `europe-west1`, `asia-northeast1` など

#### 4. モデルエラー
**エラー**: `Model not found`

**解決方法**:
- モデル名が正しいか確認（`gemini-1.5-pro` など）
- 指定した地域でモデルが利用可能か確認

### ログ確認
```bash
# アプリケーションログで詳細確認
tail -f logs/zenn_mcp/zenn_mcp.log
```

## 💰 料金情報

### Vertex AI Gemini モデルの料金（2024年7月時点）

| モデル | 入力料金 | 出力料金 |
|--------|----------|----------|
| Gemini 1.5 Pro | $0.00125 / 1K tokens | $0.00375 / 1K tokens |
| Gemini 1.5 Flash | $0.000125 / 1K tokens | $0.000375 / 1K tokens |

**料金最適化のヒント**:
- 短い要約には `gemini-1.5-flash` を使用
- `max_length` パラメータで出力トークン数を制限
- 不要なリクエストを避けるため、エラーハンドリングを適切に実装

## 🔒 セキュリティベストプラクティス

### 1. 認証情報の管理
- サービスアカウントキーは安全な場所に保存
- キーファイルは `.gitignore` に追加
- 本番環境では IAM ロールを使用（GCE、GKE等）

### 2. アクセス制御
- 最小権限の原則でサービスアカウント権限を設定
- 定期的なキーローテーション
- 監査ログの有効化

### 3. データプライバシー
- 機密データを含む記事の処理時は注意
- データ処理場所の確認（地域選択）
- Google のデータ使用ポリシーの確認

## 📋 設定チェックリスト

開発開始前の確認項目：

- [ ] Google Cloud プロジェクト作成済み
- [ ] Vertex AI API 有効化済み
- [ ] サービスアカウント作成・権限設定済み
- [ ] サービスアカウントキーダウンロード済み
- [ ] 環境変数設定済み（`GOOGLE_CLOUD_PROJECT`, `GOOGLE_APPLICATION_CREDENTIALS`）
- [ ] `.env` ファイル作成済み
- [ ] 接続テスト成功
- [ ] 料金・制限の確認済み

## 🔄 継続的インテグレーション

### GitHub Actions 設定

GitHub Secrets に以下を設定：

```
GOOGLE_CLOUD_PROJECT: your-project-id
GOOGLE_APPLICATION_CREDENTIALS_JSON: <サービスアカウントキーのJSON内容をBase64エンコード>
```

ワークフローファイル例：
```yaml
- name: Setup Google Cloud Auth
  run: |
    echo "${{ secrets.GOOGLE_APPLICATION_CREDENTIALS_JSON }}" | base64 -d > /tmp/gcp-key.json
    export GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json
    export GOOGLE_CLOUD_PROJECT=${{ secrets.GOOGLE_CLOUD_PROJECT }}
```

---

このセットアップにより、Vertex AI を使用した高品質な記事要約機能が利用可能になります。