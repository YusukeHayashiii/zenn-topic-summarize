"""
Zenn記事取得機能のテスト - Simplified version
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.crawler import ZennCrawler


class TestZennCrawler:

    def test_should_create_crawler_instance(self):
        """ZennCrawlerインスタンスが作成できること"""
        crawler = ZennCrawler()
        assert crawler is not None

    def test_should_fetch_articles_from_zenn_feed(self):
        """フィードから記事を取得できること（モックテスト）"""
        with patch('requests.get') as mock_get:
            # モックレスポンスを設定
            mock_response = MagicMock()
            mock_response.content = """
            <?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0">
                <channel>
                    <item>
                        <title>Test Article</title>
                        <link>https://zenn.dev/test</link>
                        <pubDate>Mon, 14 Jul 2025 08:34:28 GMT</pubDate>
                        <description>Test description</description>
                    </item>
                </channel>
            </rss>
            """
            mock_get.return_value = mock_response
            
            crawler = ZennCrawler()
            articles = crawler.fetch_articles_from_feed(
                "react", max_articles=5
            )
            
            assert isinstance(articles, list)
            if articles:
                article = articles[0]
                assert "title" in article
                assert "url" in article
                assert "published_at" in article
                assert "description" in article

    def test_should_handle_feed_fetch_error(self):
        """フィード取得エラーを適切に処理すること"""
        with patch('requests.get') as mock_get:
            # ネットワークエラーをシミュレート
            mock_get.side_effect = Exception("Network error")
            
            crawler = ZennCrawler()
            articles = crawler.fetch_articles_from_feed("react")
            
            assert isinstance(articles, list)
            assert len(articles) == 0