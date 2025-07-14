# SOW: プロジェクト基盤構築

## 作業概要

Zenn MCP サーバープロジェクトの基盤となる設定ファイル群とディレクトリ構造を構築する。

## 対象ブランチ

`feature/zenn_mcp_01`（developから分岐）

## 完了条件

### 必須要件
- [ ] pyproject.tomlの作成と依存関係定義
- [ ] requirements.txtの作成（pip互換性用）
- [ ] uv.lockの生成
- [ ] アプリケーション基本ディレクトリ構造の作成
- [ ] 基本的な設定ファイル（config.py）の作成
- [ ] ロギング設定（vibelogger使用）の実装
- [ ] 基本的なテスト環境の構築
- [ ] .gitignoreの更新

### 品質要件
- [ ] pytest実行可能（空のテストでも可）
- [ ] uvコマンドでの依存関係管理動作確認
- [ ] 基本的なimport確認（config, loggingなど）

## 実装予定内容

### 1. パッケージ管理設定
- `pyproject.toml`: プロジェクトメタデータ、依存関係、ツール設定
- `requirements.txt`: pip互換性用の依存関係リスト
- `uv.lock`: 依存関係のロックファイル

### 2. ディレクトリ構造
```
zenn_mcp_server/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── utils.py
│   └── logging_config.py
├── tests/
│   ├── __init__.py
│   └── test_basic.py
└── logs/
    └── zenn_mcp/
```

### 3. 基本設定ファイル
- `app/config.py`: アプリケーション設定管理
- `app/logging_config.py`: vibeloggerによるロギング設定
- `app/utils.py`: 共通ユーティリティ関数

### 4. テスト環境
- pytest設定
- 基本的なテストケース
- テスト実行確認

## 使用技術・ライブラリ

### 依存関係（予定）
- fastapi: WebフレームワークとMCP基盤
- requests: HTTP通信
- beautifulsoup4: HTMLパース
- python-dateutil: 日付処理
- pydantic: データ検証
- pytest: テスト
- vibelogger: ロギング

### 開発依存関係
- pytest
- pytest-asyncio

## 作業手順

1. TDD原則に従い、最小限のテストから開始
2. pyproject.toml作成
3. 基本ディレクトリ構造作成
4. 設定ファイル実装
5. ロギング設定実装
6. テスト環境構築
7. 動作確認

## 想定課題・リスク

### 技術的課題
- uvとpipの互換性問題
- vibeloggerの設定方法の学習
- FastAPIとMCPの統合方法

### 対処方針
- uvドキュメント参照
- vibelogger GitHubリポジトリ参照
- 段階的な実装とテスト

## 成果物

- 動作可能なプロジェクト基盤
- 基本的なテスト実行環境
- 次フェーズ（記事取得機能実装）への準備完了

## 見積もり工数

約0.5日（4時間程度）

## 次のSOW

`02_article_crawler.md` - Zenn記事取得機能の実装