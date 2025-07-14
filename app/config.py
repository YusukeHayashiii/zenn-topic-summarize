"""
Configuration module for Zenn MCP Server - Simplified version.
"""


class Config:
    """Application configuration class."""

    # Zenn Feed settings
    ZENN_FEED_BASE_URL = "https://zenn.dev/topics"
    ZENN_API_BASE_URL = "https://zenn.dev/api"

    # Crawler settings
    CRAWLER_TIMEOUT = 60