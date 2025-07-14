"""
Configuration module for Zenn MCP Server.
"""
import os


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
    
    # Vertex AI settings
    VERTEX_AI_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    VERTEX_AI_LOCATION = os.getenv("VERTEX_AI_LOCATION", "us-central1")
    VERTEX_AI_MODEL = os.getenv("VERTEX_AI_MODEL", "gemini-1.5-pro")
    
    # Google Cloud Authentication
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # LLM API settings
    SUMMARY_MAX_LENGTH = 300
    MAX_CONCURRENT_REQUESTS = 5
    REQUEST_TIMEOUT = 30
    
    # Output settings
    DEFAULT_OUTPUT_DIR = "./output"
    MARKDOWN_TEMPLATE = "default"
    
    # Crawler settings
    CRAWLER_TIMEOUT = 10
    CRAWLER_MAX_RETRY = 3
    DEFAULT_PERIOD = "week"