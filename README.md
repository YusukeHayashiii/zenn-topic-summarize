# Zenn MCP Server

Zennの記事を検索・要約してMarkdownレポートを生成するMCPサーバーです。

## 概要

このプロジェクトは、Zennの特定トピックに関する記事を取得・要約し、Markdown形式でレポートを生成するMCP（Model Context Protocol）サーバーです。Claude Codeから利用可能で、開発者の情報収集を効率化します。

## 機能

- Zenn記事の検索・取得
- LLM（Vertex AI Gemini 2.5 Pro）による記事要約
- Markdownレポート生成
- Claude Code統合

## セットアップ

```bash
# 依存関係のインストール
uv sync

# 環境変数設定
export VERTEX_AI_PROJECT_ID="your-gcp-project-id"
export VERTEX_AI_LOCATION="us-central1"
```

## 使用方法

```bash
# MCPサーバー起動
uv run python app/main.py

# テスト実行
uv run pytest
```

詳細は `CLAUDE.md` と `docs/requirements.md` をご覧ください。