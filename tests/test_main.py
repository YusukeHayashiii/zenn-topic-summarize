"""
Test main module functionality.
"""

import pytest


def test_main_module_exists():
    """Test that main module can be imported."""
    try:
        from app import main

        assert main is not None
    except ImportError:
        pytest.fail("Main module should be importable")


def test_app_instance_exists():
    """Test that FastAPI app instance exists."""
    from app.main import app

    assert app is not None


def test_app_has_correct_title():
    """Test that app has the correct title."""
    from app.main import app

    assert hasattr(app, "title")
    assert app.title == "Zenn MCP Server"


def test_health_endpoint_exists():
    """Test that health endpoint exists and is accessible."""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
