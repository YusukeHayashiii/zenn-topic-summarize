# Zenn MCP サーバー要件定義書

## 1. プロジェクト概要

### 1.1 目的
Zennの特定トピックに関する記事を取得・要約し、Markdown形式でレポートを生成するMCP（Model Context Protocol）サーバーを開発する。Claude Codeから利用可能とし、開発者の情報収集を効率化する。

### 1.2 対象ユーザー
- Claude Codeを使用する開発者
- Zennから最新技術情報を効率的に収集したいユーザー

## 2. 機能要件

### 2.1 コア機能

#### 2.1.1 記事検索・取得機能
- **入力パラメータ**
  - トピック名（必須）: 検索対象のトピック文字列
  - 期間フィルタ（オプション）: `today`, `week`, `month`, または具体的な日付範囲
  - 記事数制限（オプション）: デフォルト10件、最大50件

- **処理仕様**
  - Zennトピックフィード (`https://zenn.dev/topics/[トピック名]/feed`) を優先使用
  - フィードが利用不可の場合、Zenn非公開JSON API (`/api/articles`) を使用
  - 最終手段として、HTMLスクレイピングでフォールバック
  - いいね数（liked_count）降順でソート
  - 指定期間内の記事のみを対象
  - 上位10件（またはユーザー指定数）を抽出

#### 2.1.2 記事要約機能
- **要約対象**
  - 記事タイトル
  - 記事本文（HTML→テキスト変換後）
  - 記事メタデータ（著者、公開日、いいね数等）

- **要約仕様**
  - LLM（Google Cloud Vertex AI - Gemini 2.5 Pro）を使用した自動要約
  - モデル選択理由: 大きなコンテキストウィンドウ（2,097,152トークン）により複数記事の並列処理が可能
  - 要約長: 200-300文字程度
  - 技術的なポイントを重視
  - 並列処理による高速化

#### 2.1.3 レポート生成機能
- **出力形式**: Markdown
- **出力内容**
  - レポートヘッダー（生成日時、検索条件）
  - 記事一覧（各記事につき以下を含む）
    - タイトル
    - 著者名
    - 公開日
    - いいね数
    - 記事URL
    - 要約内容
  - フッター（取得件数、処理時間等）

- **保存機能**
  - ユーザー指定パスへの保存
  - ファイル名自動生成（日時+トピック名）
  - 既存ファイル上書き確認

### 2.2 MCP統合機能

#### 2.2.1 MCPツール定義
- `search_zenn_articles`: メイン検索機能
- `get_article_summary`: 個別記事要約
- `save_report`: レポート保存

#### 2.2.2 エラーハンドリング
- ネットワークエラー時の再試行
- API制限時の適切な待機
- 不正なパラメータの検証とエラーメッセージ

## 3. 非機能要件

### 3.1 性能要件
- 記事取得: 1記事あたり平均2秒以内
- 要約生成: 並列処理により全体で30秒以内（10記事の場合）
- レスポンス時間: 初回リクエストから結果表示まで60秒以内

### 3.2 可用性要件
- Zenn APIダウン時のフォールバック機能
- LLM API障害時の適切なエラーハンドリング
- ネットワーク不安定時の再試行機能（最大3回）

### 3.3 拡張性要件
- 新しいLLMプロバイダーの追加容易性
- 出力フォーマットの拡張可能性（JSON、CSV等）
- トピック以外の検索条件追加への対応

### 3.4 保守性要件
- 設定ファイルによる外部化可能なパラメータ
- 詳細なログ出力
- デバッグモードの提供

## 4. 技術仕様

### 4.1 アーキテクチャ
```
zenn_mcp_server/
├── app/
│   ├── __init__.py          # Pythonパッケージ初期化
│   ├── main.py              # FastAPI + MCP エントリーポイント
│   ├── crawler.py           # Zenn記事取得 (実装済み)
│   ├── summarizer.py        # 統合要約機能 (実装済み)
│   ├── renderer.py          # Markdown生成 (実装済み)
│   ├── config.py            # 設定管理 (実装済み)
│   ├── logging_config.py    # ログ設定 (実装済み)
│   ├── vertex_ai_client.py  # Vertex AI クライアント (実装済み)
│   └── utils.py             # 共通ユーティリティ (未実装)
├── tests/                   # テストコード
│   ├── __init__.py          # テストパッケージ初期化
│   ├── test_config.py       # 設定テスト (実装済み)
│   ├── test_crawler.py      # クローラーテスト (実装済み)
│   ├── test_logging.py      # ログテスト (実装済み)
│   ├── test_main.py         # メインテスト (実装済み)
│   ├── test_vertex_ai.py    # Vertex AIテスト (実装済み)
│   ├── test_summarizer.py   # 統合要約テスト (実装済み)
│   ├── test_renderer.py     # レポート生成テスト (実装済み)
│   └── test_integration.py  # 統合テスト (実装済み)
├── docs/                    # ドキュメント
│   ├── requirements.md      # 要件定義書
│   ├── tdd_rule.md         # TDD開発ルール
│   ├── branch_rule.md      # ブランチ戦略
│   ├── vertex-ai-setup.md  # Vertex AI設定手順
│   ├── github-actions-setup.md # GitHub Actions設定
│   ├── dev_log/            # 開発ログ
│   │   ├── 01_project_foundation_completed.md
│   │   ├── 02_article_crawler_implementation.md
│   │   ├── 02_vibelogger_integration_completed.md
│   │   └── 03_integrated_summarization_system_completed.md
│   ├── sow/                # 作業範囲定義書
│   │   ├── 01_project_foundation.md
│   │   ├── 02_article_crawler.md
│   │   └── 03_integrated_summarization_system.md
│   └── planning/           # 計画書
│       └── plan_o3.md
├── logs/                   # ログファイル
│   └── zenn_mcp/          # プロジェクト専用ログ
├── pyproject.toml          # uv設定・依存関係
├── uv.lock                 # 依存関係ロックファイル
├── requirements.txt        # pip用依存関係（互換性用）
├── CLAUDE.md              # Claude Code開発ルール
└── README.md             # プロジェクト説明
```

※注意：.mcp.jsonはホームディレクトリ配下（@~/.claude/.mcp.json）に配置する

### 4.2 使用技術・ライブラリ
- **Webフレームワーク**: FastAPI
- **HTTP通信**: requests
- **HTMLパース**: BeautifulSoup4 + lxml (XMLパーサー)
- **日付処理**: python-dateutil
- **データ検証**: Pydantic
- **LLM統合**: google-cloud-aiplatform (Vertex AI)
- **テスト**: pytest
- **ロギング**: loguru, vibelogger

### 4.3 外部API
- **Zenn トピックフィード**: `https://zenn.dev/topics/[トピック名]/feed`
- **Zenn API（フォールバック）**: `https://zenn.dev/api/articles`
- **LLM API**: Google Cloud Vertex AI (Gemini 2.5 Pro)

### 4.4 設定項目
```python
# config.py
class Config:
    # API設定
    ZENN_FEED_BASE_URL = "https://zenn.dev/topics"
    ZENN_API_BASE_URL = "https://zenn.dev/api"
    LLM_PROVIDER = "vertex_ai"  # Google Cloud Vertex AI
    
    # Vertex AI設定
    VERTEX_AI_PROJECT_ID = "your-gcp-project-id"
    VERTEX_AI_LOCATION = "us-central1"
    VERTEX_AI_MODEL = "gemini-2.5-pro"
    
    # 取得制限
    MAX_ARTICLES = 50
    DEFAULT_ARTICLES = 10
    SUMMARY_MAX_LENGTH = 300
    
    # 並列処理
    MAX_CONCURRENT_REQUESTS = 5
    REQUEST_TIMEOUT = 30
    
    # 出力設定
    DEFAULT_OUTPUT_DIR = "./output"
    MARKDOWN_TEMPLATE = "default"
    
    # クローラー設定
    CRAWLER_TIMEOUT = 10
    CRAWLER_MAX_RETRY = 3
    DEFAULT_PERIOD = "week"
```

## 5. インターフェース仕様

### 5.1 MCPツール仕様

#### `search_zenn_articles`
```json
{
  "name": "search_zenn_articles",
  "description": "Zennから指定トピックの記事を検索・要約してレポート生成",
  "inputSchema": {
    "type": "object",
    "properties": {
      "topic": {
        "type": "string",
        "description": "検索トピック"
      },
      "period": {
        "type": "string",
        "enum": ["today", "week", "month"],
        "description": "取得期間"
      },
      "max_articles": {
        "type": "integer",
        "minimum": 1,
        "maximum": 50,
        "default": 10,
        "description": "最大取得記事数"
      },
      "output_path": {
        "type": "string",
        "description": "保存先パス（オプション）"
      }
    },
    "required": ["topic"]
  }
}
```

### 5.2 出力フォーマット

#### Markdownレポート例
```markdown
# Zenn記事要約レポート

**検索トピック**: React
**取得期間**: 直近1週間
**生成日時**: 2024-01-15 10:30:00
**取得記事数**: 10件

---

## 1. React 18の新機能完全ガイド

- **著者**: example_user
- **公開日**: 2024-01-14
- **いいね数**: 125
- **URL**: https://zenn.dev/example/articles/react18-guide

**要約**:
React 18で導入されたConcurrent Features、Suspense、自動バッチングなどの新機能について詳細に解説。特にuseTransitionフックの使用例と性能改善効果について実践的な内容が含まれている。

---

## 2. [次の記事...]

...

---

**処理時間**: 45秒
**要約文字数**: 平均280文字
```

## 6. 品質要件

### 6.1 テスト要件
- **単体テスト**: 全関数の90%以上のカバレッジ
- **統合テスト**: MCP通信、外部API連携
- **E2Eテスト**: Claude Codeからの実行テスト

### 6.2 セキュリティ要件
- API Keyの環境変数管理
- 入力値の適切なサニタイゼーション
- レート制限の遵守

### 6.3 エラーハンドリング
- 外部API障害時の適切なエラーメッセージ
- 部分的成功時の処理継続
- ログ出力による問題追跡支援

## 7. 制約事項

### 7.1 技術制約
- Python 3.8以上
- インターネット接続必須
- LLM API利用によるコスト発生

### 7.2 利用制約
- Zenn利用規約の遵守
- API使用量制限の考慮
- 商用利用時のライセンス確認

## 8. リスク要件

### 8.1 技術リスク
| リスク | 影響度 | 対策 |
|--------|--------|------|
| Zenn API仕様変更 | 高 | HTMLスクレイピングフォールバック |
| LLM APIコスト増大 | 中 | 使用量制限・dry-runモード |
| 大量アクセスによる制限 | 中 | レート制限・キャッシュ機能 |

### 8.2 運用リスク
| リスク | 影響度 | 対策 |
|--------|--------|------|
| 利用規約違反 | 高 | 適切な間隔での取得・利用条件確認 |
| 著作権問題 | 中 | 要約のみ提供・原文リンク明記 |

## 9. 開発・運用

### 9.1 開発スケジュール
- **Phase 1**: コア機能実装（1.5日）
- **Phase 2**: MCP統合（0.5日）
- **Phase 3**: テスト・ドキュメント整備（0.5日）
- **Phase 4**: Claude Code統合テスト（0.5日）

### 9.2 運用要件
- 定期的な動作確認（週1回）
- Zenn API変更の監視
- ユーザーフィードバックの収集

## 10. 受け入れ基準

### 10.1 機能基準
- [ ] 指定トピックでの記事検索が正常動作
- [ ] 期間フィルタが正確に適用される
- [ ] いいね数順のソートが正しく実行される
- [ ] LLMによる要約が適切な品質で生成される
- [ ] Markdownレポートが正しい形式で出力される
- [ ] Claude Codeから正常に呼び出し可能

### 10.2 性能基準
- [ ] 10記事の処理が60秒以内で完了
- [ ] エラー発生時の適切な復旧処理
- [ ] メモリ使用量が合理的範囲内

### 10.3 品質基準
- [ ] 単体テストカバレッジ90%以上
- [ ] エラーケースでの適切な処理
- [ ] 分かりやすいエラーメッセージの提供

## 11. 開発タスク分解

### 11.1 基盤設定タスク
- [x] プロジェクト初期設定（pyproject.toml、uv.lock作成）
- [x] 環境変数設定とconfig.py実装
- [x] vibeloggerによるロギング設定
- [x] 基本的なテスト環境構築
- [x] .gitignore設定

### 11.2 記事取得機能タスク
- [x] Zennトピックフィード取得機能実装（基本構造）
- [ ] Zenn非公開JSON API取得機能実装（フォールバック）
- [ ] HTMLスクレイピング機能実装（最終フォールバック）
- [x] 期間フィルタ機能実装
- [x] いいね数ソート機能実装
- [x] 記事数制限機能実装
- [ ] ネットワークエラー時の再試行機能実装（部分実装）

### 11.3 記事要約機能タスク
- [x] Vertex AI (Gemini 2.5 Pro) クライアント実装（基盤）
- [x] 記事本文のHTML→テキスト変換機能実装
- [x] 複数記事の並列要約処理実装
- [x] 要約品質制御（200-300文字、技術ポイント重視）実装
- [x] LLM API障害時のエラーハンドリング実装

### 11.4 レポート生成機能タスク
- [x] Markdownテンプレート作成
- [x] レポートヘッダー生成機能実装
- [x] 記事一覧フォーマット機能実装
- [x] フッター生成機能実装
- [x] ファイル保存機能実装
- [x] ファイル名自動生成機能実装
- [x] 上書き確認機能実装

### 11.5 MCP統合機能タスク
- [x] FastAPI基盤実装
- [x] `search_zenn_articles` MCPツール実装
- [x] `get_article_summary` MCPツール実装
- [x] `save_report` MCPツール実装
- [x] パラメータ検証機能実装
- [x] エラーレスポンス機能実装
- [x] MCP通信テスト実装

### 11.6 統合・品質保証タスク
- [x] 単体テスト実装（90%カバレッジ目標）
- [x] 統合テスト実装
- [ ] E2Eテスト実装（Claude Code連携）
- [x] 性能テスト実装（60秒以内制約）
- [x] エラーケーステスト実装
- [x] ドキュメント最終整備