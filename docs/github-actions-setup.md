# GitHub Actions - Claude Code Action セットアップガイド

このドキュメントでは、Vertex AI を使用したClaude Code Actionの設定手順を説明します。

**参考記事**: [Claude Code Action を Vertex AI で動かす](https://zenn.dev/team_zenn/articles/claude-code-vertex-ai)

## 🔧 前提条件

- Google Cloud Platform プロジェクト
- Vertex AI での Claude モデルへのアクセス権
- GitHub App の作成（推奨）

## 🛠️ セットアップ手順

### 1. Vertex AI での Claude モデルアクセス設定

#### モデルアクセス権限の取得
1. [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) にアクセス
2. "Claude" で検索し、利用したいモデルを選択（ここではClaude 4 Sonnet を使用）
3. 「REQUEST ACCESS」をクリックして申請

### 2. Workload Identity Federation の設定

詳細は参考記事を閲覧されたい

#### Workload Identity Pool を作成

#### GitHub 用のプロバイダーを作成

#### サービスアカウントを作成

#### Workload Identity でサービスアカウントの権限借用を許可

### 3. GitHub Secrets の設定

GitHub リポジトリの Settings > Secrets and variables > Actions で以下を設定：

| シークレット名 | 説明 | 例 |
|---------------|------|-----|
| `APP_ID` | GitHub App ID | `12345` |
| `APP_PRIVATE_KEY` | GitHub App 秘密鍵 | `-----BEGIN RSA PRIVATE KEY-----...` |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | Workload Identity Provider | `projects/.../workloadIdentityPools/.../providers/...` |
| `GCP_SERVICE_ACCOUNT` | サービスアカウントメール | `service-account@project.iam.gserviceaccount.com` |

### 4. ワークフローファイル設定

`.github/workflows/claude-code.yml`:

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
          model: "claude-sonnet-4@20250514"
          use_vertex: "true"
          github_token: ${{ steps.app-token.outputs.token }}
          trigger_phrase: "@claude"
          timeout_minutes: "60"
        env:
          ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
          CLOUD_ML_REGION: us-east5
          BASE_BRANCH: develop
```

## 🎯 使用方法

### プルリクエストでの自動実行
- `@claude` でメンションすると Claude が応答
- 例：`@claude このプルリクエストをレビューしてください`

### 利用可能なモデル
- `claude-sonnet-4@20250514`

## 💰 料金について

- Vertex AI の Claude モデル使用料金が発生
- GitHub Actions の実行時間に応じた料金
- 詳細は Google Cloud の料金ページを参照

---

この設定により、Vertex AI を使用した高品質な Claude Code Action が利用可能になります。