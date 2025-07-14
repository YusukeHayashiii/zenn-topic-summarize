"""
Test logging configuration functionality.
"""
import pytest
import os
from pathlib import Path


def test_logging_config_module_exists():
    """Test that logging_config module can be imported."""
    try:
        from app import logging_config
        assert logging_config is not None
    except ImportError:
        pytest.fail("Logging config module should be importable")


def test_setup_logging_function_exists():
    """Test that setup_logging function exists."""
    from app.logging_config import setup_logging
    assert callable(setup_logging)


def test_setup_logging_creates_log_directory():
    """Test that setup_logging creates the log directory."""
    from app.logging_config import setup_logging
    
    # Setup logging
    setup_logging()
    
    # Check that logs directory exists
    log_dir = Path("logs/zenn_mcp")
    assert log_dir.exists()
    assert log_dir.is_dir()


def test_logger_can_write_message():
    """Test that logger can write a message after setup."""
    from app.logging_config import setup_logging, get_logger
    
    # Setup logging
    setup_logging()
    
    # Get logger and write a test message
    logger = get_logger("test")
    logger.info("Test message")
    
    # Logger should be created without errors
    assert logger is not None