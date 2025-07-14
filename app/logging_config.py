"""
Logging configuration for Zenn MCP Server.
Temporarily using standard logging until vibelogger API is confirmed.
"""
import logging
import os
from pathlib import Path


def setup_logging():
    """Setup logging configuration."""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs/zenn_mcp")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "zenn_mcp.log"),
            logging.StreamHandler()
        ]
    )


def get_logger(name: str):
    """Get a logger instance with the given name."""
    return logging.getLogger(name)