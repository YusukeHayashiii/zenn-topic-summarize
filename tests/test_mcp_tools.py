"""
MCPツールのテスト
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from mcp.types import TextContent

from app.main import (
    list_tools, 
    call_tool,
    handle_search_zenn_articles,
    handle_get_article_summary,
    handle_save_report
)


class TestMCPTools:
    """MCPツールのテストクラス"""
    
    @pytest.mark.asyncio
    async def test_list_tools_returns_correct_tools(self):
        """list_tools が正しいツールリストを返すことを確認"""
        tools = await list_tools()
        
        assert len(tools) == 3
        tool_names = [tool.name for tool in tools]
        assert "search_zenn_articles" in tool_names
        assert "get_article_summary" in tool_names
        assert "save_report" in tool_names
        
        # search_zenn_articles の詳細チェック
        search_tool = next(tool for tool in tools if tool.name == "search_zenn_articles")
        assert "topic" in search_tool.inputSchema["properties"]
        assert "period" in search_tool.inputSchema["properties"]
        assert "max_articles" in search_tool.inputSchema["properties"]
        assert search_tool.inputSchema["required"] == ["topic"]
    
    @pytest.mark.asyncio
    async def test_call_tool_routes_to_correct_handler(self):
        """call_tool が正しいハンドラーにルーティングすることを確認"""
        with patch('app.main.handle_search_zenn_articles', new_callable=AsyncMock) as mock_search:
            mock_search.return_value = [TextContent(type="text", text="test result")]
            
            result = await call_tool("search_zenn_articles", {"topic": "test"})
            
            mock_search.assert_called_once_with({"topic": "test"})
            assert len(result) == 1
            assert result[0].text == "test result"
    
    @pytest.mark.asyncio
    async def test_call_tool_unknown_tool(self):
        """未知のツール名でのcall_tool呼び出しテスト"""
        result = await call_tool("unknown_tool", {})
        
        assert len(result) == 1
        assert "Unknown tool: unknown_tool" in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_search_zenn_articles_success(self):
        """search_zenn_articles ハンドラーの正常動作テスト"""
        arguments = {
            "topic": "React",
            "period": "week",
            "max_articles": 5
        }
        
        # Mock the components
        mock_result = {
            "articles": [
                {
                    "title": "Test Article",
                    "author": "test_author",
                    "published_at": "2024-01-01",
                    "liked_count": 10,
                    "url": "https://test.com",
                    "summary": "Test summary"
                }
            ],
            "processing_time": 1.5
        }
        
        with patch('app.main.ZennCrawler'), \
             patch('app.main.ZennSummarizer') as mock_summarizer, \
             patch('app.main.MarkdownRenderer') as mock_renderer:
            
            mock_summarizer_instance = mock_summarizer.return_value
            mock_summarizer_instance.process_topic = AsyncMock(return_value=mock_result)
            
            mock_renderer_instance = mock_renderer.return_value
            mock_renderer_instance.generate_report.return_value = "# Test Report"
            
            result = await handle_search_zenn_articles(arguments)
            
            assert len(result) == 1
            assert "レポートを生成しました" in result[0].text
            assert "# Test Report" in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_search_zenn_articles_with_output_path(self):
        """output_path指定時のsearch_zenn_articles テスト"""
        arguments = {
            "topic": "React",
            "output_path": "/tmp/test_report.md"
        }
        
        mock_result = {
            "articles": [],
            "processing_time": 0.5
        }
        
        with patch('app.main.ZennCrawler'), \
             patch('app.main.ZennSummarizer') as mock_summarizer, \
             patch('app.main.MarkdownRenderer') as mock_renderer:
            
            mock_summarizer_instance = mock_summarizer.return_value
            mock_summarizer_instance.process_topic = AsyncMock(return_value=mock_result)
            
            mock_renderer_instance = mock_renderer.return_value
            mock_renderer_instance.generate_report.return_value = "# Test Report"
            mock_renderer_instance.save_report.return_value = "/tmp/test_report.md"
            
            result = await handle_search_zenn_articles(arguments)
            
            assert len(result) == 1
            assert "保存先: /tmp/test_report.md" in result[0].text
            mock_renderer_instance.save_report.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_handle_search_zenn_articles_error(self):
        """search_zenn_articles エラーハンドリングテスト"""
        arguments = {"topic": "React"}
        
        with patch('app.main.ZennCrawler') as mock_crawler:
            mock_crawler.side_effect = Exception("Test error")
            
            result = await handle_search_zenn_articles(arguments)
            
            assert len(result) == 1
            assert "エラーが発生しました" in result[0].text
            assert "Test error" in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_get_article_summary_success(self):
        """get_article_summary ハンドラーの正常動作テスト"""
        arguments = {
            "url": "https://zenn.dev/test/article",
            "summary_length": 200
        }
        
        with patch('app.main.ZennSummarizer') as mock_summarizer:
            mock_summarizer_instance = mock_summarizer.return_value
            mock_summarizer_instance.extract_article_content = AsyncMock(
                return_value="Test article content"
            )
            mock_summarizer_instance.summarize_content = AsyncMock(
                return_value="Test summary"
            )
            
            result = await handle_get_article_summary(arguments)
            
            assert len(result) == 1
            assert "記事要約:" in result[0].text
            assert "Test summary" in result[0].text
            assert arguments["url"] in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_get_article_summary_no_content(self):
        """記事内容取得失敗時のget_article_summary テスト"""
        arguments = {"url": "https://zenn.dev/test/article"}
        
        with patch('app.main.ZennSummarizer') as mock_summarizer:
            mock_summarizer_instance = mock_summarizer.return_value
            mock_summarizer_instance.extract_article_content = AsyncMock(return_value="")
            
            result = await handle_get_article_summary(arguments)
            
            assert len(result) == 1
            assert "記事の内容を取得できませんでした" in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_get_article_summary_error(self):
        """get_article_summary エラーハンドリングテスト"""
        arguments = {"url": "https://zenn.dev/test/article"}
        
        with patch('app.main.ZennSummarizer') as mock_summarizer:
            mock_summarizer.side_effect = Exception("Network error")
            
            result = await handle_get_article_summary(arguments)
            
            assert len(result) == 1
            assert "エラーが発生しました" in result[0].text
            assert "Network error" in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_save_report_success(self):
        """save_report ハンドラーの正常動作テスト"""
        arguments = {
            "content": "# Test Report Content",
            "path": "/tmp/test.md"
        }
        
        with patch('app.main.MarkdownRenderer') as mock_renderer, \
             patch('pathlib.Path.exists', return_value=False):
            
            mock_renderer_instance = mock_renderer.return_value
            mock_renderer_instance.save_report.return_value = "/tmp/test.md"
            
            result = await handle_save_report(arguments)
            
            assert len(result) == 1
            assert "レポートを保存しました: /tmp/test.md" in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_save_report_file_exists_no_overwrite(self):
        """ファイル存在時・上書きなしのsave_report テスト"""
        arguments = {
            "content": "# Test Report Content",
            "path": "/tmp/existing.md",
            "overwrite": False
        }
        
        with patch('pathlib.Path.exists', return_value=True):
            result = await handle_save_report(arguments)
            
            assert len(result) == 1
            assert "ファイルが既に存在します" in result[0].text
            assert "overwrite=trueを指定してください" in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_save_report_file_exists_with_overwrite(self):
        """ファイル存在時・上書きありのsave_report テスト"""
        arguments = {
            "content": "# Test Report Content",
            "path": "/tmp/existing.md",
            "overwrite": True
        }
        
        with patch('app.main.MarkdownRenderer') as mock_renderer, \
             patch('pathlib.Path.exists', return_value=True):
            
            mock_renderer_instance = mock_renderer.return_value
            mock_renderer_instance.save_report.return_value = "/tmp/existing.md"
            
            result = await handle_save_report(arguments)
            
            assert len(result) == 1
            assert "レポートを保存しました: /tmp/existing.md" in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_save_report_error(self):
        """save_report エラーハンドリングテスト"""
        arguments = {
            "content": "# Test Report Content",
            "path": "/invalid/path.md"
        }
        
        with patch('app.main.MarkdownRenderer') as mock_renderer, \
             patch('pathlib.Path.exists', return_value=False):
            
            mock_renderer_instance = mock_renderer.return_value
            mock_renderer_instance.save_report.side_effect = Exception("Permission denied")
            
            result = await handle_save_report(arguments)
            
            assert len(result) == 1
            assert "エラーが発生しました" in result[0].text
            assert "Permission denied" in result[0].text