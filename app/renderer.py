"""
Markdown レポート生成機能
Zenn記事要約データからMarkdownレポートを生成
"""

import os
from datetime import datetime
from typing import Dict, List
from app.logging_config import get_logger


class MarkdownRenderer:
    """Markdownレポート生成クラス"""

    def __init__(self):
        """初期化"""
        self.logger = get_logger(__name__)
        self.logger.info(
            operation="renderer_init", message="MarkdownRenderer initialized"
        )

    def generate_report(self, data: Dict) -> str:
        """
        データからMarkdownレポートを生成

        Args:
            data: 記事データ辞書

        Returns:
            生成されたMarkdownレポート
        """
        self.logger.info(
            operation="generate_report",
            message="Starting report generation",
            context={
                "topic": data.get("topic", ""),
                "articles_count": len(data.get("articles", [])),
            },
        )

        try:
            # ヘッダー生成
            header = self._generate_header(data)

            # 記事セクション生成
            articles_section = self._generate_articles_section(data.get("articles", []))

            # フッター生成
            footer = self._generate_footer(data)

            # 全体レポート組み立て
            report = f"{header}\n\n{articles_section}\n\n{footer}"

            self.logger.info(
                operation="generate_report",
                message="Report generation completed",
                context={"report_length": len(report)},
            )

            return report

        except Exception as e:
            self.logger.error(
                operation="generate_report",
                message="Report generation failed",
                context={"error": str(e), "error_type": type(e).__name__},
            )
            return "# エラー\n\nレポートの生成中にエラーが発生しました。"

    def save_report(self, data: Dict, file_path: str) -> bool:
        """
        レポートをファイルに保存

        Args:
            data: 記事データ辞書
            file_path: 保存先ファイルパス

        Returns:
            保存成功時True、失敗時False
        """
        try:
            report = self.generate_report(data)

            # ディレクトリの確認・作成
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            # ファイルに保存
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(report)

            self.logger.info(
                operation="save_report",
                message="Report saved successfully",
                context={
                    "file_path": file_path,
                    "file_size": os.path.getsize(file_path),
                },
            )

            return True

        except Exception as e:
            self.logger.error(
                operation="save_report",
                message="Report save failed",
                context={"file_path": file_path, "error": str(e)},
            )
            return False

    def generate_filename(self, topic: str) -> str:
        """
        自動ファイル名生成

        Args:
            topic: トピック名

        Returns:
            生成されたファイル名
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c for c in topic if c.isalnum() or c in ("-", "_")).strip()
        return f"zenn_report_{safe_topic}_{timestamp}.md"

    def _generate_header(self, data: Dict) -> str:
        """ヘッダー部分を生成"""
        topic = data.get("topic", "不明")
        period = self._translate_period(data.get("period", "不明"))
        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        articles_count = data.get("total_articles", len(data.get("articles", [])))

        header = f"""# Zenn記事要約レポート

**検索トピック**: {topic}
**取得期間**: {period}
**生成日時**: {generated_at}
**取得記事数**: {articles_count}件

---"""

        return header

    def _generate_articles_section(self, articles: List[Dict]) -> str:
        """記事セクション部分を生成"""
        if not articles:
            return "## 結果\n\n取得された記事はありませんでした。"

        sections = []

        for i, article in enumerate(articles, 1):
            title = article.get("title", "無題")
            author = article.get("author", "不明")
            published_at = article.get("published_at", "不明")
            liked_count = article.get("liked_count", 0)
            url = article.get("url", "")
            summary = article.get("summary", "要約がありません。")

            section = f"""## {i}. {title}

- **著者**: {author}
- **公開日**: {published_at}
- **いいね数**: {liked_count}
- **URL**: {url}

**要約**:
{summary}

---"""

            sections.append(section)

        return "\n\n".join(sections)

    def _generate_footer(self, data: Dict) -> str:
        """フッター部分を生成"""
        processing_time = data.get("processing_time", 0)
        articles = data.get("articles", [])

        # 平均要約文字数計算
        if articles:
            total_chars = sum(len(article.get("summary", "")) for article in articles)
            avg_chars = total_chars // len(articles) if articles else 0
        else:
            avg_chars = 0

        footer = f"""**処理時間**: {processing_time:.1f}秒
**要約文字数**: 平均{avg_chars}文字"""

        return footer

    def _translate_period(self, period: str) -> str:
        """期間を日本語に翻訳"""
        translations = {"today": "本日", "week": "直近1週間", "month": "直近1ヶ月"}
        return translations.get(period, "未指定")
