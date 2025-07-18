# SOW: シンプルなZennフィード取得機能

## プロジェクト概要

Zennのトピック別フィードを取得し、記事の基本情報（タイトル、作成日、概要、URL）を出力するシンプルな機能を開発する。

## 背景

- 当初計画していたURL指定による記事要約機能が技術的に困難であることが判明
- スコープを絞り、Zennフィードの取得と基本情報の表示に特化する
- MCPツールとしてシンプルで使いやすい機能を提供する

## 機能要件

### 主要機能
1. **トピック指定によるフィード取得**
   - ユーザーがトピック名を指定
   - 指定されたトピックでZennのフィードを取得

2. **記事情報の出力**
   - タイトル (title)
   - 作成日 (pubDate)
   - 概要 (description)
   - URL (link)

3. **件数制限**
   - 最大10件の記事を取得・表示

## 技術仕様

### API設計
- 既存の `search_zenn_articles` ツールを修正
- レスポンス形式をシンプルに変更
- 要約機能を除去し、フィード情報のみ返却

### データ構造
```python
{
    "topic": str,
    "articles": [
        {
            "title": str,
            "pubDate": str,
            "description": str,
            "link": str
        }
    ],
    "count": int
}
```

## 実装範囲

### 対応項目
- [ ] 既存 `search_zenn_articles` ツールの修正
- [ ] フィード取得ロジックの簡素化
- [ ] レスポンス形式の変更
- [ ] エラーハンドリングの改善
- [ ] テストケースの追加

### 対応外項目
- 記事内容の取得・要約
- レポート生成機能
- ファイル保存機能

## 品質要件

### 機能要件
- 指定されたトピックで正確にフィードを取得
- 10件以内で記事情報を返却
- エラー時の適切な処理

### 非機能要件
- レスポンス時間: 5秒以内
- エラー率: 1%以下
- 可用性: 95%以上

## リスク分析

### 技術リスク
- ZennのフィードURL構造の変更 (中)
- RSS/XMLパースエラー (低)

### 対策
- フィードURL取得の冗長化
- エラーハンドリングの強化

## 開発スケジュール

### Phase 1: 実装 (1-2日)
- 既存コードの修正
- テストケース作成

### Phase 2: テスト・調整 (1日)
- 動作確認
- パフォーマンス調整

## 受け入れ基準

### 機能面
- [ ] トピック指定でフィード取得が可能
- [ ] 記事の基本情報（title, pubDate, description, link）が正確に表示
- [ ] 最大10件の制限が正しく動作
- [ ] エラー時に適切なメッセージが表示

### 技術面
- [ ] テストカバレッジ80%以上
- [ ] エラーハンドリングが適切に実装
- [ ] ログ出力が適切（vibelogger使用）

## 完了条件

1. すべての受け入れ基準をクリア
2. テストが全て通る
3. ドキュメントが更新済み
4. MCPツールとして正常に動作確認済み