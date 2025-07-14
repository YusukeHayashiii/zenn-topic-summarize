"""
Zenn記事統合要約システム
記事取得、本文抽出、要約、統合処理を担当
"""

import time
import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from app.crawler import ZennCrawler
from app.vertex_ai_client import VertexAIClient
from app.logging_config import get_logger


class ZennSummarizer:
    """Zenn記事の統合要約システム"""

    def __init__(self):
        """初期化"""
        self.crawler = ZennCrawler()
        self.vertex_ai_client = VertexAIClient()
        self.logger = get_logger(__name__)
        self.logger.info(
            operation="summarizer_init", message="ZennSummarizer initialized"
        )

    def process_topic(
        self, topic: str, period: str = "week", max_articles: int = 10
    ) -> Dict:
        """
        トピックを処理して記事取得・要約・統合処理を実行

        Args:
            topic: 検索トピック
            period: 期間フィルタ
            max_articles: 最大記事数

        Returns:
            処理結果辞書

        Raises:
            ValueError: トピックが空の場合
        """
        if not topic or topic.strip() == "":
            raise ValueError("Topic cannot be empty")

        self.logger.info(
            operation="process_topic",
            message="Starting topic processing",
            context={"topic": topic, "period": period, "max_articles": max_articles},
        )
        start_time = time.time()

        try:
            # 記事取得
            articles = self.crawler.fetch_articles(topic, max_articles=max_articles)[
                :max_articles
            ]

            # 各記事の要約処理
            processed_articles = []
            for article in articles:
                try:
                    summary = self._summarize_article(article)
                    processed_article = {**article, "summary": summary}
                    processed_articles.append(processed_article)
                except Exception as e:
                    self.logger.warning(
                        operation="article_summarization",
                        message="Failed to summarize article",
                        context={
                            "article_title": article.get("title", ""),
                            "error": str(e),
                        },
                    )
                    # 要約に失敗した場合もタイトルだけは含める
                    processed_article = {
                        **article,
                        "summary": "要約の生成に失敗しました。",
                    }
                    processed_articles.append(processed_article)

            processing_time = time.time() - start_time

            result = {
                "topic": topic,
                "period": period,
                "articles": processed_articles,
                "processing_time": processing_time,
                "total_articles": len(processed_articles),
            }

            self.logger.info(
                operation="process_topic",
                message="Topic processing completed",
                context={
                    "processing_time": processing_time,
                    "articles_processed": len(processed_articles),
                },
            )
            return result

        except Exception as e:
            self.logger.error(
                operation="process_topic",
                message="Topic processing failed",
                context={"error": str(e), "error_type": type(e).__name__},
            )
            raise

    def _summarize_article(self, article: Dict) -> str:
        """
        記事を要約する

        Args:
            article: 記事情報辞書

        Returns:
            要約テキスト
        """
        try:
            # 記事本文を取得
            content = self._extract_article_content(article["url"])

            if not content:
                return "記事本文の取得に失敗しました。"

            # 要約生成
            summary = self.vertex_ai_client.summarize_text(content)
            return summary

        except Exception as e:
            self.logger.warning(
                operation="article_summarization",
                message="Article summarization failed",
                context={"error": str(e), "article_url": article.get("url", "")},
            )
            return "要約の生成中にエラーが発生しました。"

    def _extract_article_content(self, url: str) -> str:
        """
        記事URLから本文を抽出

        Args:
            url: 記事URL

        Returns:
            抽出されたテキスト
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return self._html_to_text(response.content.decode("utf-8"))

        except Exception as e:
            self.logger.warning(
                operation="content_extraction",
                message="Content extraction failed",
                context={"url": url, "error": str(e)},
            )
            return ""

    def _html_to_text(self, html_content: str) -> str:
        """
        HTMLをテキストに変換

        Args:
            html_content: HTML文字列

        Returns:
            変換されたテキスト
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # 不要なタグを削除
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()

            # テキストを抽出
            text = soup.get_text()

            # 改行と空白の整理
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = " ".join(chunk for chunk in chunks if chunk)

            return text

        except Exception as e:
            self.logger.warning(
                operation="html_to_text",
                message="HTML to text conversion failed",
                context={"error": str(e)},
            )
            return ""
