# Zenn MCP Server

Zennの記事フィードを取得するMCPサーバーです。

## 概要

このプロジェクトは、Zennの特定トピックに関する記事フィードを取得するMCP（Model Context Protocol）サーバーです。Claude Codeから利用可能で、開発者の情報収集を効率化します。

## 機能

- Zenn記事フィードの取得
- Claude Code統合（1つのMCPツール提供）

## 🚀 初期設定

### 1. プロジェクトのクローン

```bash
git clone https://github.com/YusukeHayashiii/zenn-topic-summarize.git
cd zenn_mcp_dev
```

### 2. 依存関係のインストール

```bash
# uvが未インストールの場合
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
uv sync
```

### 3. Claude Code MCP設定

`.mcp.json` に以下を追加：

```json
{
  "mcpServers": {
    "zenn-mcp": {
        "command": "uv",
        "args": [
          "--directory",
          "/path/to/zenn_mcp_dev",
          "run",
          "app/main.py"
        ]
      }
  }
}
```

**注意**: 

-  `/path/to/zenn_mcp_dev` を実際のプロジェクトディレクトリのパスに変更してください。
-  `.mcp.json` の追加場所については[公式サイト](https://docs.anthropic.com/ja/docs/claude-code/settings#%E8%A8%AD%E5%AE%9A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB)を参照

### 4. 動作確認

MCPサーバーが正常に起動すれば、Claude Codeから以下のツールが利用可能になります：
- `search_zenn_articles`: 指定トピックの記事フィード取得

## 🎯 使用方法

### Claude Codeでの使用例

初期セットアップ完了後は、Claude Codeを普通に起動するだけで利用可能です。

```
Reactについて最新の記事フィードを取得してください
```

Claude Codeが自動的に `search_zenn_articles` ツールを使用して：
1. Zennから「React」トピックの記事フィードを取得
2. 記事のタイトル、URL、投稿日、作成者、概要を返却


## 🔧 トラブルシューティング

| 問題 | 解決方法 |
|------|----------|
| `ModuleNotFoundError` | `uv sync` で依存関係を再インストール |
| Claude Codeでツールが見つからない | `~/.claude/.mcp.json` のパス設定を確認 |

## 📄 ライセンス

MIT License
