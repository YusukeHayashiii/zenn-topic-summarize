"""
FastMCP実装のメインモジュールテスト
"""

import pytest
from unittest.mock import patch, Mock

from app.main import mcp, search_zenn_articles


class TestMainModule:
    """メインモジュールのテストクラス"""
    
    def test_main_module_exists(self):
        """メインモジュールが存在することを確認"""
        import app.main
        assert app.main is not None
    
    def test_fastmcp_instance_exists(self):
        """FastMCPインスタンスが存在することを確認"""
        assert mcp is not None
        assert mcp.name == "zenn-mcp"
    
    def test_search_zenn_articles_function_exists(self):
        """search_zenn_articles関数が存在することを確認"""
        assert callable(search_zenn_articles)
    
    def test_search_zenn_articles_success(self):
        """search_zenn_articles関数の正常動作テスト"""
        mock_articles = [
            {
                "title": "React基礎講座",
                "published_at": "2024-01-15",
                "description": "Reactの基本的な使い方を学ぼう",
                "url": "https://zenn.dev/sample/articles/react-basics"
            },
            {
                "title": "React Hooks入門",
                "published_at": "2024-01-14", 
                "description": "React Hooksの活用方法",
                "url": "https://zenn.dev/sample/articles/react-hooks"
            }
        ]
        
        with patch('app.main.ZennCrawler') as mock_crawler:
            mock_crawler_instance = mock_crawler.return_value
            mock_crawler_instance.fetch_articles_from_feed.return_value = mock_articles
            
            result = search_zenn_articles("React", 5)
            
            assert "トピック: React" in result
            assert "取得記事数: 2件" in result
            assert "React基礎講座" in result
            assert "React Hooks入門" in result
    
    def test_search_zenn_articles_no_articles(self):
        """記事が見つからない場合のテスト"""
        with patch('app.main.ZennCrawler') as mock_crawler:
            mock_crawler_instance = mock_crawler.return_value
            mock_crawler_instance.fetch_articles_from_feed.return_value = []
            
            result = search_zenn_articles("NonExistentTopic", 5)
            
            assert "記事が見つかりませんでした" in result
            assert "NonExistentTopic" in result
    
    def test_search_zenn_articles_error_handling(self):
        """エラーハンドリングのテスト"""
        with patch('app.main.ZennCrawler') as mock_crawler:
            mock_crawler_instance = mock_crawler.return_value
            mock_crawler_instance.fetch_articles_from_feed.side_effect = Exception("Network error")
            
            result = search_zenn_articles("React", 5)
            
            assert "エラーが発生しました" in result
            assert "Network error" in result
    
    def test_search_zenn_articles_max_articles_validation(self):
        """max_articlesの値検証テスト"""
        mock_articles = [{"title": "Test Article", "published_at": "2024-01-01", "description": "Test", "url": "http://test.com"}]
        
        with patch('app.main.ZennCrawler') as mock_crawler:
            mock_crawler_instance = mock_crawler.return_value
            mock_crawler_instance.fetch_articles_from_feed.return_value = mock_articles
            
            # 上限を超えた値をテスト
            result = search_zenn_articles("React", 15)
            mock_crawler_instance.fetch_articles_from_feed.assert_called_with(topic="React", max_articles=10)
            
            # 下限を下回った値をテスト  
            result = search_zenn_articles("React", -1)
            mock_crawler_instance.fetch_articles_from_feed.assert_called_with(topic="React", max_articles=10)