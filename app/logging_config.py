"""
Logging configuration for Zenn MCP Server using vibelogger.
"""

from vibelogger import create_file_logger

# Global logger instance
_logger = None


def setup_logging():
    """Setup vibelogger configuration."""
    global _logger

    # Create vibelogger instance - it automatically creates ./logs/zenn_mcp/ directory
    _logger = create_file_logger("zenn_mcp")


def get_logger(name: str = "zenn_mcp"):
    """Get the vibelogger instance."""
    if _logger is None:
        setup_logging()
    return _logger
