"""
Tests for GET /activities endpoint.
Follows AAA pattern: Arrange, Act, Assert.
"""

import pytest


def test_get_activities_returns_200(client):
    """
    Arrange: TestClient ready.
    Act: GET /activities
    Assert: Status 200 and activities returned.
    """
    # Arrange - implicit via fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_activities_returns_correct_structure(client):
    """
    Arrange: TestClient ready with default activities.
    Act: GET /activities
    Assert: Response contains expected activity fields and structure.
    """
    # Arrange - implicit via fixture

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities
    
    # Verify structure of an activity
    chess = activities["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_get_activities_participants_list_has_initial_data(client):
    """
    Arrange: TestClient ready.
    Act: GET /activities
    Assert: Initial participants are present in the response.
    """
    # Arrange - implicit via fixture

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    chess = activities["Chess Club"]
    assert len(chess["participants"]) == 2
    assert "michael@mergington.edu" in chess["participants"]
    assert "daniel@mergington.edu" in chess["participants"]
