# SOW: MCP統合機能実装

## 1. 作業概要

ZennMCPサーバーにMCP（Model Context Protocol）統合機能を実装し、Claude Codeからの呼び出しを可能にする。

## 2. 完了条件

- [ ] FastAPI基盤にMCP通信機能を統合
- [ ] `search_zenn_articles` MCPツールが正常動作
- [ ] `get_article_summary` MCPツールが正常動作  
- [ ] `save_report` MCPツールが正常動作
- [ ] パラメータ検証とエラーハンドリングが適切に実装
- [ ] MCP通信のテストケースが実装され、全て通過
- [ ] Claude Codeから実際に呼び出し可能

## 3. 実装対象

### 3.1 MCPツール実装
- `search_zenn_articles`: メイン検索・要約・レポート生成機能
- `get_article_summary`: 個別記事要約機能
- `save_report`: レポート保存機能

### 3.2 統合機能
- パラメータ検証（Pydantic）
- エラーレスポンス処理
- 既存機能（crawler, summarizer, renderer）との統合

### 3.3 テスト実装
- MCPツールの単体テスト
- 統合テスト
- エラーケーステスト

## 4. 技術仕様

### 4.1 MCPツール仕様

#### `search_zenn_articles`
```json
{
  "name": "search_zenn_articles",
  "description": "Zennから指定トピックの記事を検索・要約してレポート生成",
  "inputSchema": {
    "type": "object",
    "properties": {
      "topic": {"type": "string", "description": "検索トピック"},
      "period": {"type": "string", "enum": ["today", "week", "month"], "description": "取得期間"},
      "max_articles": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
      "output_path": {"type": "string", "description": "保存先パス（オプション）"}
    },
    "required": ["topic"]
  }
}
```

#### `get_article_summary`
```json
{
  "name": "get_article_summary",
  "description": "指定記事URLの内容を要約",
  "inputSchema": {
    "type": "object",
    "properties": {
      "url": {"type": "string", "description": "記事URL"},
      "summary_length": {"type": "integer", "default": 300}
    },
    "required": ["url"]
  }
}
```

#### `save_report`
```json
{
  "name": "save_report",
  "description": "レポートをファイルに保存",
  "inputSchema": {
    "type": "object",
    "properties": {
      "content": {"type": "string", "description": "レポート内容"},
      "path": {"type": "string", "description": "保存先パス"},
      "overwrite": {"type": "boolean", "default": false}
    },
    "required": ["content", "path"]
  }
}
```

## 5. 実装手順

1. **MCPライブラリの統合**
   - 必要な依存関係追加
   - FastAPIアプリケーションにMCP機能統合

2. **MCPツール実装**
   - 各ツールの実装
   - パラメータ検証
   - エラーハンドリング

3. **テスト実装**
   - 単体テスト
   - 統合テスト
   - エラーケーステスト

4. **統合テスト**
   - 既存機能との連携確認
   - 性能テスト

## 6. リスク・注意事項

- MCP通信プロトコルの正確な実装が必要
- 既存機能（crawler, summarizer, renderer）との統合時の互換性確保
- Claude Codeとの通信テストは実機でのみ可能

## 7. 成果物

- 実装済みコード（app/main.py更新、新規ファイル追加）
- テストコード（tests/test_mcp_*.py）
- 統合テスト結果
- Claude Code連携設定手順書更新

## 8. 受け入れ基準

- [ ] 全MCPツールがClaude Codeから正常呼び出し可能
- [ ] パラメータエラー時の適切なエラーメッセージ表示
- [ ] 既存機能との連携が正常動作
- [ ] 単体テスト・統合テストが全て通過
- [ ] 性能要件（60秒以内）を満たす