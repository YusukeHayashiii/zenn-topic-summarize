"""
Test cases for Zenn Article Summarizer
TDD implementation following Red-Green-Refactor cycle
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.summarizer import ZennSummarizer


class TestZennSummarizer:
    """Test cases for ZennSummarizer class"""

    @pytest.fixture
    def mock_crawler(self):
        """Mock crawler fixture"""
        mock = Mock()
        mock.fetch_articles.return_value = [
            {
                "title": "React Hooks詳解",
                "url": "https://zenn.dev/sample/articles/react-hooks",
                "author": "tech_user",
                "published_at": "2024-01-15",
                "liked_count": 42,
            },
            {
                "title": "TypeScript実践ガイド",
                "url": "https://zenn.dev/sample/articles/typescript-guide",
                "author": "dev_user",
                "published_at": "2024-01-14",
                "liked_count": 35,
            },
        ]
        return mock

    @pytest.fixture
    def mock_vertex_ai(self):
        """Mock Vertex AI client fixture"""
        mock = Mock()
        mock.summarize_text.return_value = "これはReact Hooksの要約です。"
        return mock

    @pytest.fixture
    def summarizer(self, mock_crawler, mock_vertex_ai):
        """Summarizer fixture with mocked dependencies"""
        with patch("app.summarizer.ZennCrawler", return_value=mock_crawler), patch(
            "app.summarizer.VertexAIClient", return_value=mock_vertex_ai
        ):
            return ZennSummarizer()

    def test_summarizer_initialization(self, summarizer):
        """Test summarizer properly initializes"""
        assert summarizer is not None
        assert hasattr(summarizer, "crawler")
        assert hasattr(summarizer, "vertex_ai_client")

    def test_process_topic_basic_functionality(self, summarizer):
        """Test basic topic processing functionality"""
        # Red: This should fail initially
        result = summarizer.process_topic("React", max_articles=2)

        assert result is not None
        assert isinstance(result, dict)
        assert "articles" in result
        assert "topic" in result
        assert len(result["articles"]) == 2

    def test_process_topic_with_period_filter(self, summarizer):
        """Test topic processing with period filter"""
        result = summarizer.process_topic("React", period="week", max_articles=1)

        assert result["topic"] == "React"
        assert result["period"] == "week"
        assert len(result["articles"]) == 1

    def test_article_content_extraction(self, summarizer):
        """Test HTML content extraction from article URL"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.content = (
                b"<html><body><p>Article content here</p></body></html>"
            )
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            content = summarizer._extract_article_content("https://example.com/article")

            assert content is not None
            assert "Article content here" in content

    def test_html_to_text_conversion(self, summarizer):
        """Test HTML to text conversion"""
        html_content = """
        <html>
            <body>
                <h1>記事タイトル</h1>
                <p>これは段落1です。</p>
                <p>これは段落2です。</p>
                <div>不要なdiv</div>
            </body>
        </html>
        """

        text = summarizer._html_to_text(html_content)

        assert "記事タイトル" in text
        assert "これは段落1です。" in text
        assert "これは段落2です。" in text
        # HTML tagsが除去されていることを確認
        assert "<html>" not in text
        assert "<p>" not in text

    def test_summarization_integration(self, summarizer, mock_vertex_ai):
        """Test article summarization integration"""
        article = {
            "title": "React Hooks詳解",
            "url": "https://zenn.dev/sample/articles/react-hooks",
            "author": "tech_user",
            "published_at": "2024-01-15",
            "liked_count": 42,
        }

        with patch.object(
            summarizer, "_extract_article_content", return_value="記事本文内容"
        ):
            summary = summarizer._summarize_article(article)

            assert summary is not None
            assert summary == "これはReact Hooksの要約です。"
            mock_vertex_ai.summarize_text.assert_called_once()

    def test_error_handling_for_failed_content_extraction(self, summarizer):
        """Test error handling when content extraction fails"""
        with patch("requests.get", side_effect=Exception("Network error")):
            content = summarizer._extract_article_content("https://invalid-url.com")

            # エラー時は空文字列またはNoneを返すべき
            assert content == "" or content is None

    def test_batch_processing_multiple_articles(self, summarizer):
        """Test batch processing of multiple articles"""
        result = summarizer.process_topic("React", max_articles=2)

        # 複数記事の処理結果を確認
        assert len(result["articles"]) == 2
        for article in result["articles"]:
            assert "title" in article
            assert "summary" in article
            assert "url" in article

    def test_processing_time_tracking(self, summarizer):
        """Test processing time is tracked"""
        result = summarizer.process_topic("React", max_articles=1)

        assert "processing_time" in result
        assert isinstance(result["processing_time"], (int, float))
        assert result["processing_time"] >= 0

    def test_empty_topic_handling(self, summarizer):
        """Test handling of empty or invalid topic"""
        with pytest.raises(ValueError, match="Topic cannot be empty"):
            summarizer.process_topic("")

    def test_max_articles_limit_enforcement(self, summarizer):
        """Test max articles limit is enforced"""
        result = summarizer.process_topic("React", max_articles=1)

        assert len(result["articles"]) <= 1

    @patch("app.summarizer.get_logger")
    def test_logging_functionality(self, mock_logger, summarizer):
        """Test proper logging functionality"""
        summarizer.process_topic("React", max_articles=1)

        # ログが呼び出されたことを確認
        mock_logger.return_value.info.assert_called()
