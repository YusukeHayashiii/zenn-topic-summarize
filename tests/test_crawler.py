"""
Zenn記事取得機能のテスト
TDD Red-Green-Refactorサイクルに従って実装
"""

import pytest
from unittest.mock import Mock, patch
from app.crawler import ZennCrawler


class TestZennCrawler:
    
    def test_should_create_crawler_instance(self):
        """ZennCrawlerインスタンスが作成できること"""
        crawler = ZennCrawler()
        assert crawler is not None
        
    def test_should_fetch_articles_by_topic(self):
        """指定したトピックの記事を取得できること"""
        crawler = ZennCrawler()
        articles = crawler.fetch_articles("react")
        
        # 基本的な検証
        assert isinstance(articles, list)
        assert len(articles) > 0
        
        # 記事の構造検証
        article = articles[0]
        assert "title" in article
        assert "url" in article
        assert "author" in article
        assert "published_at" in article
        assert "liked_count" in article
    
    def test_should_fetch_articles_from_zenn_feed(self):
        """Zennフィードから記事を取得できること"""
        crawler = ZennCrawler()
        
        # 期間フィルタと記事数制限のテスト
        articles = crawler.fetch_articles_from_feed("react", period="week", max_articles=5)
        
        assert isinstance(articles, list)
        assert len(articles) <= 5
        
        if len(articles) > 0:
            article = articles[0]
            assert "title" in article
            assert "url" in article 
            assert "author" in article
            assert "published_at" in article
            assert "liked_count" in article
    
    def test_should_sort_articles_by_liked_count(self):
        """記事をいいね数順でソートできること"""
        crawler = ZennCrawler()
        articles = crawler.fetch_articles("react", max_articles=3)
        
        if len(articles) >= 2:
            # いいね数が降順になっているか確認
            for i in range(len(articles) - 1):
                assert articles[i]["liked_count"] >= articles[i + 1]["liked_count"]