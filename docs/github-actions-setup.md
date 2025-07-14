# GitHub Actions - Claude Code Review セットアップガイド

このドキュメントでは、GitHub ActionsでClaude Code Reviewを設定する手順を説明します。

## 🔧 必要な環境変数の設定

### 1. Anthropic API Keyの取得と設定

#### API Keyの取得
1. [Anthropic Console](https://console.anthropic.com/) にアクセス
2. アカウントにログインまたは新規登録
3. 「API Keys」セクションに移動
4. 「Create Key」をクリックして新しいAPIキーを生成
5. 生成されたAPIキーをコピー（一度しか表示されません）

#### GitHub Secretsへの追加
1. GitHubリポジトリにアクセス
2. 「Settings」タブをクリック
3. 左サイドバーの「Secrets and variables」→「Actions」をクリック
4. 「New repository secret」をクリック
5. 以下の情報を入力：
   - **Name**: `ANTHROPIC_API_KEY`
   - **Secret**: 取得したAnthropic APIキー
6. 「Add secret」をクリック

### 2. GitHub Token (自動設定済み)

`GITHUB_TOKEN`は GitHub Actions で自動的に提供されるため、手動設定は不要です。

## 🚀 ワークフロー設定

### ファイル構成
```
.github/
├── workflows/
│   └── claude-code-review.yml    # メインワークフロー
└── claude-code-config.yml        # Claude設定ファイル
```

### トリガー条件
ワークフローは以下の条件で実行されます：
- プルリクエストが作成された時（`opened`）
- プルリクエストが更新された時（`synchronize`）
- プルリクエストが再オープンされた時（`reopened`）
- 対象ブランチ：`main`, `develop`

### レビュー対象ファイル
以下のファイルタイプがレビューされます：
- Python ファイル（`*.py`）
- JavaScript/TypeScript ファイル（`*.js`, `*.ts`, `*.jsx`, `*.tsx`）
- 設定ファイル（`*.yml`, `*.yaml`, `*.json`, `*.toml`）
- ドキュメント（`*.md`）

## 🎯 レビューフォーカス

Claude Code Reviewは以下の観点でコードをレビューします：

### 1. コード品質
- PEP 8準拠（Python）
- ベストプラクティスの遵守
- コードの可読性と保守性

### 2. テスト品質
- TDD原則の遵守
- テストカバレッジ
- テストケースの妥当性

### 3. セキュリティ
- 脆弱性の検出
- セキュリティベストプラクティス
- API セキュリティ

### 4. パフォーマンス
- パフォーマンスの最適化提案
- LLM統合の効率性

### 5. ドキュメント
- ドキュメントの完全性
- コメントの適切性

## 🔍 使用方法

### 1. プルリクエスト作成
通常通りプルリクエストを作成すると、自動的にClaude Code Reviewが実行されます。

### 2. レビュー結果の確認
- **ライン別コメント**: 具体的な改善提案がコードの該当行に表示
- **サマリーコメント**: プルリクエスト全体の概要コメントが投稿
- **ステータスチェック**: PRのチェック状況が更新

### 3. レビュー結果への対応
1. Claude の提案を確認
2. 必要に応じてコードを修正
3. 修正をプッシュすると再度レビューが実行

## 🛠️ カスタマイズ

### 設定ファイルの編集
`.github/claude-code-config.yml` を編集して以下をカスタマイズできます：
- レビューフォーカス領域
- ファイルパターン（include/exclude）
- コメント設定
- AI モデル設定

### ワークフローの調整
`.github/workflows/claude-code-review.yml` を編集して以下を調整できます：
- トリガー条件
- 実行ブランチ
- 権限設定
- カスタム指示

## 📋 トラブルシューティング

### よくある問題

#### 1. API Key関連
**問題**: `Error: Missing or invalid Anthropic API key`
**解決策**: 
- GitHub Secrets に `ANTHROPIC_API_KEY` が正しく設定されているか確認
- APIキーが有効で、使用量制限に達していないか確認

#### 2. 権限関連
**問題**: `Error: Insufficient permissions to comment on PR`
**解決策**:
- ワークフローファイルの `permissions` セクションを確認
- リポジトリの Actions 権限設定を確認

#### 3. ファイルが除外される
**問題**: 期待したファイルがレビューされない
**解決策**:
- `.github/claude-code-config.yml` の `patterns` セクションを確認
- `include` および `exclude` パターンを調整

### ログの確認
GitHub Actions の「Actions」タブでワークフローの実行ログを確認できます。

## 🔄 継続的改善

### メトリクス追跡
- レビューの精度
- 発見された問題の重要度
- 開発者の満足度

### 設定の調整
定期的に以下を見直します：
- フォーカス領域の調整
- 除外パターンの最適化
- コメント品質の改善

## 📚 参考リンク

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Claude Code Review Action](https://github.com/anthropic/claude-code-review-action)

## ⚠️ 注意事項

1. **APIコスト**: Claude API の使用には料金が発生します
2. **プライバシー**: コードがAnthropic のサービスに送信されます
3. **レート制限**: API の使用量制限にご注意ください
4. **セキュリティ**: 機密情報を含むリポジトリでの使用は慎重に検討してください

---

このセットアップにより、プルリクエストごとに自動的にClaude による高品質なコードレビューが実行されます。