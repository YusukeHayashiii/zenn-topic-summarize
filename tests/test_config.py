"""
Test configuration module - Simplified version.
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
    """Test that Config class has all required attributes."""
    from app.config import Config
    
    # Check that required attributes exist
    assert hasattr(Config, "ZENN_FEED_BASE_URL")
    assert hasattr(Config, "ZENN_API_BASE_URL")
    assert hasattr(Config, "CRAWLER_TIMEOUT")


def test_config_default_values():
    """Test that Config has correct default values."""
    from app.config import Config
    
    assert Config.ZENN_FEED_BASE_URL == "https://zenn.dev/topics"
    assert Config.ZENN_API_BASE_URL == "https://zenn.dev/api"
    assert Config.CRAWLER_TIMEOUT == 60