"""
Main FastAPI application for Zenn MCP Server.
"""

import asyncio
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from app.config import Config
from app.crawler import ZennCrawler
from app.logging_config import setup_logging, get_logger
from app.renderer import MarkdownRenderer
from app.summarizer import ZennSummarizer

# Initialize logging
setup_logging()
logger = get_logger(__name__)

# Create MCP server
mcp_server = Server("zenn-mcp")

# Create FastAPI app instance
app = FastAPI(
    title="Zenn MCP Server",
    description="MCP Server for Zenn article search, summarization and report generation",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# MCP Tools implementation
@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="search_zenn_articles",
            description="Zennから指定トピックの記事を検索・要約してレポート生成",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "検索トピック"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["today", "week", "month"],
                        "description": "取得期間",
                        "default": "week"
                    },
                    "max_articles": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 10,
                        "description": "最大取得記事数"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "保存先パス（オプション）"
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="get_article_summary",
            description="指定記事URLの内容を要約",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "記事URL"
                    },
                    "summary_length": {
                        "type": "integer",
                        "default": 300,
                        "description": "要約長"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="save_report", 
            description="レポートをファイルに保存",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "レポート内容"
                    },
                    "path": {
                        "type": "string",
                        "description": "保存先パス"
                    },
                    "overwrite": {
                        "type": "boolean",
                        "default": False,
                        "description": "上書き許可"
                    }
                },
                "required": ["content", "path"]
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle MCP tool calls."""
    logger.info(
        operation="mcp_tool_call",
        message=f"Tool called: {name}",
        context={"tool_name": name, "arguments": arguments}
    )
    
    if name == "search_zenn_articles":
        return await handle_search_zenn_articles(arguments)
    elif name == "get_article_summary":
        return await handle_get_article_summary(arguments)
    elif name == "save_report":
        return await handle_save_report(arguments)
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def handle_search_zenn_articles(arguments: dict) -> list[TextContent]:
    """Handle search_zenn_articles tool call."""
    try:
        topic = arguments["topic"]
        period = arguments.get("period", "week")
        max_articles = arguments.get("max_articles", 10)
        output_path = arguments.get("output_path")
        
        # Initialize components
        crawler = ZennCrawler()
        summarizer = ZennSummarizer()
        renderer = MarkdownRenderer()
        
        # Process articles
        result = await summarizer.process_topic(
            topic=topic,
            period=period,
            max_articles=max_articles
        )
        
        # Generate report
        report_content = renderer.generate_report(
            topic=topic,
            period=period,
            articles=result["articles"],
            processing_time=result["processing_time"]
        )
        
        # Save report if path specified
        if output_path:
            saved_path = renderer.save_report(
                content=report_content,
                output_path=output_path
            )
            return [TextContent(
                type="text",
                text=f"レポートを生成しました。\n\n保存先: {saved_path}\n\n{report_content}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"レポートを生成しました。\n\n{report_content}"
            )]
            
    except Exception as e:
        logger.error(
            operation="search_zenn_articles",
            message="Tool execution failed",
            context={"error": str(e)}
        )
        return [TextContent(
            type="text",
            text=f"エラーが発生しました: {str(e)}"
        )]


async def handle_get_article_summary(arguments: dict) -> list[TextContent]:
    """Handle get_article_summary tool call."""
    try:
        url = arguments["url"]
        summary_length = arguments.get("summary_length", 300)
        
        summarizer = ZennSummarizer()
        
        # Extract and summarize article content
        content = await summarizer.extract_article_content(url)
        if not content:
            return [TextContent(
                type="text",
                text="記事の内容を取得できませんでした。"
            )]
            
        summary = await summarizer.summarize_content(
            content=content,
            max_length=summary_length
        )
        
        return [TextContent(
            type="text",
            text=f"記事要約:\n\nURL: {url}\n\n{summary}"
        )]
        
    except Exception as e:
        logger.error(
            operation="get_article_summary",
            message="Tool execution failed",
            context={"error": str(e)}
        )
        return [TextContent(
            type="text",
            text=f"エラーが発生しました: {str(e)}"
        )]


async def handle_save_report(arguments: dict) -> list[TextContent]:
    """Handle save_report tool call."""
    try:
        content = arguments["content"]
        path = arguments["path"]
        overwrite = arguments.get("overwrite", False)
        
        renderer = MarkdownRenderer()
        
        # Check if file exists and overwrite is not allowed
        if Path(path).exists() and not overwrite:
            return [TextContent(
                type="text",
                text=f"ファイルが既に存在します: {path}\noverwrite=trueを指定してください。"
            )]
        
        saved_path = renderer.save_report(
            content=content,
            output_path=path
        )
        
        return [TextContent(
            type="text",
            text=f"レポートを保存しました: {saved_path}"
        )]
        
    except Exception as e:
        logger.error(
            operation="save_report",
            message="Tool execution failed",
            context={"error": str(e)}
        )
        return [TextContent(
            type="text",
            text=f"エラーが発生しました: {str(e)}"
        )]


async def run_mcp_server():
    """Run MCP server."""
    logger.info(
        operation="mcp_server_start",
        message="Starting Zenn MCP Server"
    )
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )


if __name__ == "__main__":
    # Check if running as MCP server or FastAPI server
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--mcp":
        # Run as MCP server
        asyncio.run(run_mcp_server())
    else:
        # Run as FastAPI server
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)