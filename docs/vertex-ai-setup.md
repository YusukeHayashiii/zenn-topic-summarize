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

<!-- サービスアカウントを作成し、権限借用する形にしたいので、その内容を後ほど追記する -->

## 🛠️ アプリケーション設定

### 1. 環境変数設定

以下の環境変数を設定します：

```bash
# 必須設定
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"

# オプション設定（デフォルト値あり）
export VERTEX_AI_LOCATION="us-central1"  # デフォルト: us-central1
export VERTEX_AI_MODEL="gemini-2.5-pro"  # デフォルト: gemini-2.5-pro
```

### 2. .env ファイル作成

プロジェクトルートに `.env` ファイルを作成：

```bash
# .env
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
VERTEX_AI_LOCATION=us-central1
VERTEX_AI_MODEL=gemini-2.5-pro
```

**注意**: `.env` ファイルは `.gitignore` に含まれているため、リポジトリにコミットされません。

### 3. 利用可能なモデル

Vertex AI で利用可能な Gemini モデル：

| モデル名 | 説明 | 推奨用途 |
|---------|------|---------|
| `gemini-2.5-pro` | 高性能な汎用モデル | 複雑な要約・分析 |
| `gemini-2.5-flash` | コストが安い | 簡単な要約 |

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

## 🤖 Claude Code Action セットアップ

### Claude Code Action とは

Claude Code Action は GitHub Actions 上で Anthropic の Claude モデルを活用し、プルリクエストレビュー、コード分析、コミット支援などを自動化する機能です。Vertex AI バックエンドを使用することで、Google Cloud Platform 上で Claude モデルを利用できます。

### 前提条件

Claude Code Action を使用するには以下が必要です：
- Google Cloud Platform プロジェクト
- Vertex AI での Claude モデルへのアクセス権
- GitHub リポジトリとGitHub Actions の使用権限

### 1. Vertex AI での Claude モデルアクセス設定

#### モデルアクセス権限の取得
1. [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) にアクセス
2. "Claude" で検索し、利用したいモデルを選択
   - Claude 3.5 Sonnet
   - Claude 3.5 Haiku
   - Claude 3 Opus
3. 「REQUEST ACCESS」をクリック
4. 利用目的を入力し申請（承認に時間がかかる場合があります）

#### 必要な権限の確認
サービスアカウントに以下の権限が必要です：
- `roles/aiplatform.user` - Vertex AI User
- `roles/aiplatform.admin` - AI Platform Administrator（管理者権限が必要な場合）
- `roles/ml.admin` - ML Engine Admin（レガシー権限）

### 2. Workload Identity Federation の設定

#### Workload Identity Pool の作成
```bash
# Workload Identity Pool を作成
gcloud iam workload-identity-pools create "claude-github-pool" \
    --project="${GOOGLE_CLOUD_PROJECT}" \
    --location="global" \
    --display-name="Claude GitHub Actions Pool"

# GitHub 用のプロバイダーを作成
gcloud iam workload-identity-pools providers create-oidc "claude-github-provider" \
    --project="${GOOGLE_CLOUD_PROJECT}" \
    --location="global" \
    --workload-identity-pool="claude-github-pool" \
    --display-name="Claude GitHub Provider" \
    --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
    --issuer-uri="https://token.actions.githubusercontent.com"
```

#### サービスアカウントとの関連付け
```bash
# サービスアカウントに Workload Identity User 権限を付与
gcloud iam service-accounts add-iam-policy-binding "zenn-mcp-vertex-ai@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --project="${GOOGLE_CLOUD_PROJECT}" \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/claude-github-pool/attribute.repository/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME"
```

### 3. GitHub Secrets の設定

GitHub リポジトリの Settings > Secrets and variables > Actions で以下のシークレットを設定：

| シークレット名 | 説明 | 例 |
|---------------|------|-----|
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | Workload Identity Provider のリソース名 | `projects/123456789/locations/global/workloadIdentityPools/claude-github-pool/providers/claude-github-provider` |
| `GCP_SERVICE_ACCOUNT` | サービスアカウントのメールアドレス | `zenn-mcp-vertex-ai@your-project.iam.gserviceaccount.com` |
| `GOOGLE_CLOUD_PROJECT` | Google Cloud プロジェクト ID | `your-gcp-project-id` |

### 4. GitHub Actions ワークフロー設定

`.github/workflows/claude-code.yml` を作成：

```yaml
name: Claude Code Action

permissions:
  contents: write
  pull-requests: write
  issues: write
  id-token: write

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

jobs:
  claude-pr:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Generate GitHub App token
        id: app-token
        uses: actions/create-github-app-token@v2
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Authenticate to Google Cloud
        id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

      - uses: anthropics/claude-code-action@beta
        with:
          model: "claude-3-5-sonnet@20241022"
          use_vertex: "true"
          github_token: ${{ steps.app-token.outputs.token }}
          trigger_phrase: "@claude"
          timeout_minutes: "60"
        env:
          ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
          CLOUD_ML_REGION: us-east5
          BASE_BRANCH: develop
```

### 5. トリガー設定

Claude Code Action は以下の条件で動作します：

#### プルリクエストでの自動実行
- プルリクエストが作成・更新されたとき
- `@claude` でメンションされたとき

#### コメントでの手動実行
```markdown
@claude このプルリクエストをレビューしてください

@claude コードの品質を改善する提案をお願いします

@claude セキュリティ上の問題をチェックしてください
```

### 6. 設定の検証

#### ワークフロー実行の確認
1. テストプルリクエストを作成
2. GitHub Actions タブで実行状況を確認
3. 認証エラーがないか確認

#### ログでの確認事項
- Google Cloud 認証の成功
- Vertex AI API へのアクセス成功
- Claude モデルからのレスポンス受信

---

このセットアップにより、Vertex AI を使用した高品質な記事要約機能が利用可能になります。
