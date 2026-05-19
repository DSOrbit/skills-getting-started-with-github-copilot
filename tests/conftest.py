"""
Pytest configuration and shared fixtures for backend tests.
Provides TestClient and resets in-memory state before each test.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient connected to the FastAPI app.
    Resets the in-memory activities state before each test to ensure isolation.
    """
    # Store the original activities state
    original_activities = deepcopy(activities)
    
    # Yield the client for the test to use
    yield TestClient(app)
    
    # Reset activities to original state after test completes
    activities.clear()
    activities.update(original_activities)
