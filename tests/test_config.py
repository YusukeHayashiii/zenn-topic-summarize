"""
Test config module functionality.
"""

import pytest


def test_config_module_exists():
    """Test that config module can be imported."""
    try:
        from app import config

        assert config is not None
    except ImportError:
        pytest.fail("Config module should be importable")


def test_config_has_required_attributes():
    """Test that config has required configuration attributes."""
    from app.config import Config

    # Test basic configuration attributes exist
    assert hasattr(Config, "ZENN_FEED_BASE_URL")
    assert hasattr(Config, "MAX_ARTICLES")
    assert hasattr(Config, "DEFAULT_ARTICLES")

    # Test Vertex AI configuration attributes exist
    assert hasattr(Config, "VERTEX_AI_PROJECT_ID")
    assert hasattr(Config, "VERTEX_AI_LOCATION")
    assert hasattr(Config, "VERTEX_AI_MODEL")


def test_config_default_values():
    """Test config default values are correct."""
    from app.config import Config

    assert Config.DEFAULT_ARTICLES == 10
    assert Config.MAX_ARTICLES == 50
    assert Config.ZENN_FEED_BASE_URL == "https://zenn.dev/topics"


def test_vertex_ai_config_defaults():
    """Test Vertex AI configuration default values."""
    from app.config import Config

    # Test default Vertex AI settings
    assert Config.VERTEX_AI_LOCATION == "us-central1"  # Default when env var not set
    assert Config.VERTEX_AI_MODEL == "gemini-1.5-pro"  # Default model
    assert Config.LLM_PROVIDER == "vertex_ai"
