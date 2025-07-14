"""
Main FastAPI application for Zenn MCP Server.
"""

from fastapi import FastAPI
from app.logging_config import setup_logging

# Initialize logging
setup_logging()

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
