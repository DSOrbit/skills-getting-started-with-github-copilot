"""
Tests for POST /activities/{activity_name}/signup endpoint.
Follows AAA pattern: Arrange, Act, Assert.
"""

import pytest


def test_signup_new_participant_happy_path(client):
    """
    Arrange: TestClient ready, activity exists, new email prepared.
    Act: POST /activities/Chess Club/signup?email=alice@mergington.edu
    Assert: Status 200, success message, participant added.
    """
    # Arrange
    new_email = "alice@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert new_email in data["message"]
    assert activity_name in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert new_email in activities[activity_name]["participants"]


def test_signup_returns_correct_message(client):
    """
    Arrange: TestClient ready, activity and email prepared.
    Act: POST /activities/Programming Class/signup
    Assert: Response message format is correct.
    """
    # Arrange
    new_email = "bob@mergington.edu"
    activity_name = "Programming Class"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    expected_message = f"Signed up {new_email} for {activity_name}"
    assert data["message"] == expected_message


def test_signup_nonexistent_activity_returns_404(client):
    """
    Arrange: TestClient ready, activity does not exist.
    Act: POST /activities/Nonexistent Activity/signup
    Assert: Status 404, error detail provided.
    """
    # Arrange
    email = "student@mergington.edu"
    activity_name = "Nonexistent Activity"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_multiple_different_participants(client):
    """
    Arrange: TestClient ready, activity prepared.
    Act: POST signup for two different emails.
    Assert: Both participants added successfully.
    """
    # Arrange
    email1 = "charlie@mergington.edu"
    email2 = "diana@mergington.edu"
    activity_name = "Gym Class"

    # Act
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email1}
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email2}
    )

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify both are in activity
    activities_response = client.get("/activities")
    activities = activities_response.json()
    participants = activities[activity_name]["participants"]
    assert email1 in participants
    assert email2 in participants
