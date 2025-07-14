"""
Configuration module for Zenn MCP Server.
"""


class Config:
    """Application configuration class."""
    
    # Zenn API settings
    ZENN_FEED_BASE_URL = "https://zenn.dev/topics"
    ZENN_API_BASE_URL = "https://zenn.dev/api"
    
    # Article limits
    MAX_ARTICLES = 50
    DEFAULT_ARTICLES = 10
    
    # LLM settings
    LLM_PROVIDER = "vertex_ai"
    
    # Output settings
    DEFAULT_OUTPUT_DIR = "./output"
    MARKDOWN_TEMPLATE = "default"