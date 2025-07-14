"""
Test Vertex AI integration functionality.
"""

import pytest
from unittest.mock import patch, MagicMock


def test_vertex_ai_client_module_exists():
    """Test that vertex_ai_client module can be imported."""
    try:
        from app import vertex_ai_client

        assert vertex_ai_client is not None
    except ImportError:
        pytest.fail("Vertex AI client module should be importable")


@patch("app.vertex_ai_client.aiplatform.init")
@patch("app.vertex_ai_client.gapic.PredictionServiceClient")
def test_vertex_ai_client_initialization(mock_client, mock_init):
    """Test that Vertex AI client can be initialized."""
    from app.vertex_ai_client import VertexAIClient

    # Mock the environment variables and config
    with patch.dict(
        "os.environ",
        {"GOOGLE_CLOUD_PROJECT": "test-project", "VERTEX_AI_LOCATION": "us-central1"},
    ), patch("app.vertex_ai_client.Config") as mock_config:
        mock_config.VERTEX_AI_PROJECT_ID = "test-project"
        mock_config.VERTEX_AI_LOCATION = "us-central1"
        mock_config.VERTEX_AI_MODEL = "gemini-1.5-pro"

        client = VertexAIClient()
        assert client is not None
        assert client.project_id == "test-project"
        assert client.location == "us-central1"


@patch("google.cloud.aiplatform.gapic.PredictionServiceClient")
def test_vertex_ai_client_has_summarize_method(mock_client):
    """Test that client has summarize method."""
    from app.vertex_ai_client import VertexAIClient

    with patch.dict("os.environ", {"GOOGLE_CLOUD_PROJECT": "test-project"}):
        client = VertexAIClient()
        assert hasattr(client, "summarize_text")
        assert callable(client.summarize_text)


@patch("google.cloud.aiplatform.gapic.PredictionServiceClient")
def test_vertex_ai_summarize_text_structure(mock_client):
    """Test the structure of summarize_text method."""
    from app.vertex_ai_client import VertexAIClient

    with patch.dict("os.environ", {"GOOGLE_CLOUD_PROJECT": "test-project"}):
        client = VertexAIClient()

        # Mock the prediction response
        mock_response = MagicMock()
        mock_response.predictions = [{"content": "Test summary content"}]
        mock_client.return_value.predict.return_value = mock_response

        # Test method signature
        result = client.summarize_text("Test content", max_length=200)
        assert result is not None
