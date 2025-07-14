"""
Zenn MCP Server using FastMCP for simplified implementation.
"""

from typing import Annotated

from mcp.server.fastmcp import FastMCP

from app.config import Config
from app.crawler import ZennCrawler
from app.logging_config import setup_logging, get_logger

# Initialize logging
setup_logging()
logger = get_logger(__name__)

# Create FastMCP server
mcp = FastMCP("zenn-mcp")


@mcp.tool()
def search_zenn_articles(
    topic: Annotated[str, "検索トピック"], 
    max_articles: Annotated[int, "最大取得記事数 (1-10)"] = 10
) -> str:
    """Zennから指定トピックの記事フィードを取得"""
    
    logger.info(
        operation="search_zenn_articles",
        message=f"Searching articles for topic: {topic}",
        context={"topic": topic, "max_articles": max_articles}
    )
    
    try:
        # Validate max_articles
        if max_articles < 1 or max_articles > 10:
            max_articles = 10
        
        # Initialize crawler
        crawler = ZennCrawler()
        
        # Fetch articles from feed
        articles = crawler.fetch_articles_from_feed(
            topic=topic,
            max_articles=max_articles
        )
        
        if not articles:
            return f"トピック '{topic}' の記事が見つかりませんでした。"
        
        # Format response with basic article information
        response_parts = [
            f"# トピック: {topic}",
            f"取得記事数: {len(articles)}件\n"
        ]
        
        for i, article in enumerate(articles, 1):
            response_parts.append(
                f"## {i}. {article.get('title', 'タイトルなし')}\n"
                f"- **作成日**: {article.get('published_at', '不明')}\n"
                f"- **概要**: {article.get('description', '概要なし')}\n"
                f"- **URL**: {article.get('url', 'URLなし')}\n"
            )
        
        return "\n".join(response_parts)
            
    except Exception as e:
        logger.error(
            operation="search_zenn_articles",
            message="Tool execution failed",
            context={"error": str(e)}
        )
        return f"エラーが発生しました: {str(e)}"


if __name__ == "__main__":
    logger.info(
        operation="mcp_server_start",
        message="Starting Zenn MCP Server with FastMCP"
    )
    mcp.run()