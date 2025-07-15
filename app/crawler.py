"""
Zenn記事取得機能
TDD原則に従って実装
"""

import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from app.logging_config import get_logger
from app.config import Config


class ZennCrawler:
    """Zennから記事を取得するクローラー"""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info(operation="crawler_init", message="ZennCrawler initialized")
        self.base_feed_url = Config.ZENN_FEED_BASE_URL
        self.api_base_url = Config.ZENN_API_BASE_URL
        self.trending_feed_url = Config.ZENN_TRENDING_FEED_URL
        self.timeout = Config.CRAWLER_TIMEOUT


    def fetch_articles_from_feed(
        self, topic: str, max_articles: int = None
    ) -> List[Dict]:
        """
        Zennトピックフィードから記事を取得する

        Args:
            topic: 検索対象のトピック名
            max_articles: 最大取得記事数

        Returns:
            記事リスト
        """
        max_articles = max_articles or 10

        self.logger.info(
            operation="fetch_from_feed",
            message="Fetching from feed",
            context={"topic": topic, "max_articles": max_articles},
        )

        feed_url = f"{self.base_feed_url}/{topic}/feed"

        try:
            response = requests.get(feed_url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")

            articles = []

            for item in items[:max_articles]:  # 指定数だけ取得
                try:
                    article = self._parse_feed_item(item)
                    if article:
                        articles.append(article)
                except Exception as e:
                    self.logger.warning(
                        operation="parse_feed_item",
                        message="Failed to parse feed item",
                        context={"error": str(e)},
                    )
                    continue

            self.logger.info(
                operation="fetch_from_feed",
                message="Successfully fetched articles from feed",
                context={"articles_count": len(articles)},
            )
            return articles

        except Exception as e:
            self.logger.error(
                operation="fetch_from_feed",
                message="Failed to fetch from feed",
                context={"error": str(e)},
            )
            return []

    def _parse_feed_item(self, item) -> Optional[Dict]:
        """フィードアイテムをパースして記事情報を抽出"""
        try:
            title = item.find("title").text if item.find("title") else ""
            link = item.find("link").text if item.find("link") else ""
            pub_date = item.find("pubDate").text if item.find("pubDate") else ""
            
            # dc:creator要素から作成者情報を取得
            creator = ""
            creator_element = item.find("dc:creator")
            if creator_element:
                creator = creator_element.text or ""
            
            # description要素からdescriptionテキストを取得
            description = ""
            desc_element = item.find("description")
            if desc_element:
                description = desc_element.text or ""
                # HTMLタグが含まれている場合は除去
                if "<" in description:
                    try:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(description, "html.parser")
                        description = soup.get_text().strip()
                    except:
                        description = description.replace("<", "").replace(">", "")

            return {
                "title": title,
                "url": link,
                "published_at": pub_date,
                "creator": creator,
                "description": description,
            }
        except Exception as e:
            self.logger.warning(
                operation="parse_feed_item",
                message="Failed to parse feed item",
                context={"error": str(e)},
            )
            return None

    def fetch_trending_articles(self, max_articles: int = None) -> List[Dict]:
        """
        Zennトレンドフィードから記事を取得する

        Args:
            max_articles: 最大取得記事数

        Returns:
            記事リスト
        """
        max_articles = max_articles or 10

        self.logger.info(
            operation="fetch_trending_articles",
            message="Fetching trending articles",
            context={"max_articles": max_articles},
        )

        try:
            response = requests.get(self.trending_feed_url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")

            articles = []

            for item in items[:max_articles]:  # 指定数だけ取得
                try:
                    article = self._parse_feed_item(item)
                    if article:
                        articles.append(article)
                except Exception as e:
                    self.logger.warning(
                        operation="parse_trending_item",
                        message="Failed to parse trending feed item",
                        context={"error": str(e)},
                    )
                    continue

            self.logger.info(
                operation="fetch_trending_articles",
                message="Successfully fetched trending articles",
                context={"articles_count": len(articles)},
            )
            return articles

        except Exception as e:
            self.logger.error(
                operation="fetch_trending_articles",
                message="Failed to fetch trending articles",
                context={"error": str(e)},
            )
            return []


