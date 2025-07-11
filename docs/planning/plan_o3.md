# Zenn MCP サーバー実装計画（o3 検証）

## 1. 目的
Zenn の特定トピック記事を取得し、要約結果を Markdown として保存できる Python 製 **MCP (Model Context Protocol) サーバー** を作成し、Claude Code から利用可能にする。

## 2. 技術検証まとめ
### 2.1 記事取得可否
| 方法 | 可否 | メモ |
|------|------|------|
| 非公開 JSON API (`/api/articles` エンドポイント) | ◎ | 無認証・JSON で title / liked_count / published_at など取得可 |
| HTML スクレイピング | ○ | SSR ページなので BeautifulSoup で抽出容易 |

> 公式 SDK は無いが **無認証で十分取得可能**。

### 2.2 要件別評価
* **トピック指定**: query param で対応
* **10 件制限 & いいね順**: liked_count で sort → head(10)
* **期間フィルタ**: published_at を datetime で比較
* **要約生成**: Claude / OpenAI 呼び出しで対応 (サーバー側 Proxy)
* **Markdown 出力 & 任意保存先**: FastAPI エンドポイントで `output_path` を受け取り保存

→ **全要件とも実装可能**。

## 3. システム構成案
```
app/
 ├─ main.py          # FastAPI + MCP adapter
 ├─ crawler.py       # Zenn API 呼び出し / スクレイピング
 ├─ summarizer.py    # LLM ラッパ
 └─ renderer.py      # Markdown 生成
```
### フロー
1. `crawler.get_articles(topic, since)`
2. liked_count でソートし 10 件抽出
3. 並列で全文取得 → `summarizer.summary(text)`
4. `renderer.to_markdown(...)`
5. 指定パスへ保存 & レスポンス返却

### MCP 対応
* `.mcp.json` に base_url を記述
* `main.py` で OpenAPI (fastapi) 自動公開
* 既存 mcp-atlassian の servers パターンを流用

## 4. 想定ライブラリ
* requests, beautifulsoup4
* python-dateutil, pydantic
* fastapi, uvicorn
* anthropic / openai SDK

## 5. 懸念・対策
| 懸念 | 対策 |
|------|------|
| Zenn API 仕様変更 | 失敗時は HTML スクレイピングへフォールバック |
| アクセス過多 | page サイズ調整・キャッシュ導入 |
| LLM コスト | dry-run モード・記事数/文字数制限 |

## 6. 工数見積もり
| タスク | 目安 |
|--------|------|
| クローラ実装 & テスト | 0.5 日 |
| 要約ラッパー実装 | 0.5 日 |
| Markdown テンプレート | 0.25 日 |
| FastAPI + MCP 化 | 0.5 日 |
| リファクタ & ドキュメント | 0.25 日 |
| **合計** | **約 2 日** |

## 7. 次のアクション
1. `zenn_mcp_dev/app` ディレクトリ作成
2. crawler/summarizer/renderer 各モジュール実装
3. FastAPI サーバー (`main.py`) 作成
4. `.mcp.json` をプロジェクトルートに配置し、Claude Code から呼び出しテスト
5. README 追記 & サンプルコマンド整備 