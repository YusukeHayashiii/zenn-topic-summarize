"""
Integration tests for the complete Zenn MCP system
Tests the full flow from article fetching to report generation
"""

import pytest
import tempfile
import os
from unittest.mock import patch, Mock
from app.summarizer import ZennSummarizer
from app.renderer import MarkdownRenderer


class TestIntegration:
    """統合テスト"""

    @pytest.fixture
    def mock_requests_get(self):
        """Mock HTTP requests"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.content = (
                b"<html><body><p>Test article content</p></body></html>"
            )
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            yield mock_get

    @pytest.fixture
    def mock_vertex_ai(self):
        """Mock Vertex AI client"""
        with patch("app.vertex_ai_client.VertexAIClient") as mock_client:
            mock_instance = Mock()
            mock_instance.summarize_text.return_value = "これは自動生成された要約です。"
            mock_client.return_value = mock_instance
            yield mock_instance

    def test_end_to_end_workflow(self, mock_requests_get, mock_vertex_ai):
        """エンドツーエンドのワークフローテスト"""
        # 1. Summarizerで記事取得・要約
        summarizer = ZennSummarizer()
        result = summarizer.process_topic("React", max_articles=2)

        # 2. 結果の検証
        assert result["topic"] == "React"
        assert len(result["articles"]) == 2
        assert "processing_time" in result

        # 3. Rendererでレポート生成
        renderer = MarkdownRenderer()
        report = renderer.generate_report(result)

        # 4. レポート内容の検証
        assert "# Zenn記事要約レポート" in report
        assert "React" in report
        assert "Sample React Article 1" in report

        # 5. ファイル保存テスト
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            success = renderer.save_report(result, temp_path)
            assert success is True
            assert os.path.exists(temp_path)

            with open(temp_path, "r", encoding="utf-8") as f:
                saved_content = f.read()
                assert "# Zenn記事要約レポート" in saved_content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_error_handling_integration(self, mock_vertex_ai):
        """エラーハンドリングの統合テスト"""
        # ネットワークエラーをシミュレーション
        with patch("requests.get", side_effect=Exception("Network error")):
            summarizer = ZennSummarizer()
            result = summarizer.process_topic("TestTopic", max_articles=1)

            # エラーがあっても処理が継続されることを確認
            assert result["topic"] == "TestTopic"
            assert len(result["articles"]) >= 1  # サンプルデータが返される

            # レポート生成も正常に動作することを確認
            renderer = MarkdownRenderer()
            report = renderer.generate_report(result)
            assert "# Zenn記事要約レポート" in report

    def test_large_dataset_handling(self, mock_requests_get, mock_vertex_ai):
        """大量データの処理テスト"""
        summarizer = ZennSummarizer()

        # 最大記事数での処理
        result = summarizer.process_topic("LargeDataset", max_articles=10)

        assert len(result["articles"]) <= 10
        assert result["processing_time"] >= 0

        # レポート生成
        renderer = MarkdownRenderer()
        report = renderer.generate_report(result)

        # レポートが適切な長さで生成されることを確認
        assert len(report) > 1000  # 最小限の長さ
        assert report.count("##") >= len(result["articles"])  # 各記事にセクションがある
