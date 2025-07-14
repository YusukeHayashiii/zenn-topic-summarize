"""
Test cases for Markdown Report Renderer
TDD implementation following Red-Green-Refactor cycle
"""

import pytest
import os
import tempfile
from datetime import datetime
from unittest.mock import patch, Mock
from app.renderer import MarkdownRenderer


class TestMarkdownRenderer:
    """Test cases for MarkdownRenderer class"""

    @pytest.fixture
    def sample_data(self):
        """Sample data for testing"""
        return {
            "topic": "React",
            "period": "week",
            "articles": [
                {
                    "title": "React Hooks詳解",
                    "url": "https://zenn.dev/sample/articles/react-hooks",
                    "author": "tech_user",
                    "published_at": "2024-01-15",
                    "liked_count": 42,
                    "summary": "React Hooksの基本的な使い方と応用について詳細に解説。useStateやuseEffectの実践的な活用方法を紹介。",
                },
                {
                    "title": "TypeScript実践ガイド",
                    "url": "https://zenn.dev/sample/articles/typescript-guide",
                    "author": "dev_user",
                    "published_at": "2024-01-14",
                    "liked_count": 35,
                    "summary": "TypeScriptの型システムを活用した実践的な開発手法。ジェネリクスや条件型について解説。",
                },
            ],
            "processing_time": 45.2,
            "total_articles": 2,
        }

    @pytest.fixture
    def renderer(self):
        """Renderer fixture"""
        return MarkdownRenderer()

    def test_renderer_initialization(self, renderer):
        """Test renderer properly initializes"""
        assert renderer is not None
        assert hasattr(renderer, "generate_report")

    def test_generate_report_basic_structure(self, renderer, sample_data):
        """Test basic markdown report generation"""
        # Red: This should fail initially
        report = renderer.generate_report(sample_data)

        assert report is not None
        assert isinstance(report, str)
        assert "# Zenn記事要約レポート" in report
        assert "React" in report
        assert "直近1週間" in report or "week" in report

    def test_report_header_generation(self, renderer, sample_data):
        """Test report header contains required information"""
        report = renderer.generate_report(sample_data)

        # ヘッダー情報の確認
        assert "**検索トピック**: React" in report
        assert "**取得期間**:" in report
        assert "**生成日時**:" in report
        assert "**取得記事数**: 2件" in report

    def test_article_section_formatting(self, renderer, sample_data):
        """Test individual article sections are properly formatted"""
        report = renderer.generate_report(sample_data)

        # 記事セクションの確認
        assert "## 1. React Hooks詳解" in report
        assert "## 2. TypeScript実践ガイド" in report
        assert "- **著者**: tech_user" in report
        assert "- **公開日**: 2024-01-15" in report
        assert "- **いいね数**: 42" in report
        assert "- **URL**: https://zenn.dev/sample/articles/react-hooks" in report

    def test_summary_section_inclusion(self, renderer, sample_data):
        """Test summary sections are included"""
        report = renderer.generate_report(sample_data)

        assert "**要約**:" in report
        assert "React Hooksの基本的な使い方" in report
        assert "TypeScriptの型システムを活用" in report

    def test_footer_information(self, renderer, sample_data):
        """Test footer contains processing information"""
        report = renderer.generate_report(sample_data)

        # フッター情報の確認
        assert "**処理時間**: 45.2秒" in report or "45.2" in report
        assert "**要約文字数**:" in report

    def test_save_report_functionality(self, renderer, sample_data):
        """Test saving report to file"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as temp_file:
            temp_path = temp_file.name

        try:
            result = renderer.save_report(sample_data, temp_path)

            assert result is True
            assert os.path.exists(temp_path)

            # ファイル内容の確認
            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
                assert "# Zenn記事要約レポート" in content
                assert "React" in content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_automatic_filename_generation(self, renderer, sample_data):
        """Test automatic filename generation"""
        filename = renderer.generate_filename(sample_data["topic"])

        assert filename is not None
        assert filename.endswith(".md")
        assert "React" in filename
        assert len(filename) > 10  # 日時が含まれることを確認

    def test_period_translation(self, renderer):
        """Test period translation to Japanese"""
        assert renderer._translate_period("today") == "本日"
        assert renderer._translate_period("week") == "直近1週間"
        assert renderer._translate_period("month") == "直近1ヶ月"
        assert renderer._translate_period("unknown") == "未指定"

    def test_empty_articles_handling(self, renderer):
        """Test handling of empty articles list"""
        empty_data = {
            "topic": "EmptyTopic",
            "period": "week",
            "articles": [],
            "processing_time": 1.0,
            "total_articles": 0,
        }

        report = renderer.generate_report(empty_data)

        assert "取得された記事はありませんでした" in report or "0件" in report

    def test_special_characters_handling(self, renderer):
        """Test handling of special characters in article data"""
        special_data = {
            "topic": "Test & Symbols",
            "period": "week",
            "articles": [
                {
                    "title": "記事タイトル <with> symbols & entities",
                    "url": "https://example.com/test",
                    "author": "test_user",
                    "published_at": "2024-01-15",
                    "liked_count": 1,
                    "summary": "特殊文字 & エンティティを含む要約テスト < > \" '",
                }
            ],
            "processing_time": 1.0,
            "total_articles": 1,
        }

        report = renderer.generate_report(special_data)

        # 特殊文字が適切にエスケープされているかテスト
        assert "Test & Symbols" in report
        assert "<with>" in report or "&lt;with&gt;" in report

    def test_file_overwrite_handling(self, renderer, sample_data):
        """Test file overwrite handling"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as temp_file:
            temp_path = temp_file.name
            temp_file.write("Existing content")

        try:
            # デフォルトでは上書きされるべき
            result = renderer.save_report(sample_data, temp_path)
            assert result is True

            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
                assert "Existing content" not in content
                assert "# Zenn記事要約レポート" in content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_invalid_path_error_handling(self, renderer, sample_data):
        """Test error handling for invalid file paths"""
        invalid_path = "/nonexistent/directory/report.md"

        result = renderer.save_report(sample_data, invalid_path)

        # エラーが適切に処理されることを確認
        assert result is False

    @patch("app.renderer.get_logger")
    def test_logging_functionality(self, mock_logger, renderer, sample_data):
        """Test proper logging functionality"""
        renderer.generate_report(sample_data)

        # ログが呼び出されたことを確認
        mock_logger.return_value.info.assert_called()

    def test_markdown_escaping(self, renderer):
        """Test proper markdown escaping"""
        # Markdownの特殊文字がエスケープされることをテスト
        dangerous_data = {
            "topic": "Test",
            "period": "week",
            "articles": [
                {
                    "title": "Title with **bold** and *italic* and `code`",
                    "url": "https://example.com",
                    "author": "user",
                    "published_at": "2024-01-15",
                    "liked_count": 1,
                    "summary": "Summary with # header and [link](url)",
                }
            ],
            "processing_time": 1.0,
            "total_articles": 1,
        }

        report = renderer.generate_report(dangerous_data)

        # Markdown記法がエスケープされているか確認
        assert (
            "\\*\\*bold\\*\\*" in report
            or "**bold**" not in report
            or report.count("**") == report.count("\\*\\*") * 2
        )
