"""
Basic tests for the search tools. Run with: pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.tools import search_web, search_wikipedia


def test_search_web_returns_results():
    results = search_web("quantum computing", max_results=2)
    assert len(results) > 0
    assert "title" in results[0]
    assert "url" in results[0]
    assert results[0]["source_type"] == "web"


def test_search_wikipedia_returns_results():
    results = search_wikipedia("quantum computing", max_results=2)
    assert len(results) > 0
    assert "title" in results[0]
    assert results[0]["source_type"] == "wikipedia"