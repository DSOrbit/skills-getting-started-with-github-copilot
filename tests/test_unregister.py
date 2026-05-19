"""
Tests for DELETE /activities/{activity_name}/signup endpoint.
Follows AAA pattern: Arrange, Act, Assert.
"""

import pytest


def test_unregister_existing_participant_happy_path(client):
    """
    Arrange: TestClient ready, participant already signed up.
    Act: DELETE /activities/Chess Club/signup?email=michael@mergington.edu
    Assert: Status 200, participant removed.
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Verify participant exists initially
    response_before = client.get("/activities")
    assert email in response_before.json()[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    
    # Verify participant was removed
    response_after = client.get("/activities")
    assert email not in response_after.json()[activity_name]["participants"]


def test_unregister_returns_correct_message(client):
    """
    Arrange: TestClient ready, participant ready to unregister.
    Act: DELETE /activities/Programming Class/signup
    Assert: Response message format is correct.
    """
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    expected_message = f"Unregistered {email} from {activity_name}"
    assert data["message"] == expected_message


def test_unregister_nonexistent_participant_returns_404(client):
    """
    Arrange: TestClient ready, participant not in activity.
    Act: DELETE /activities/Chess Club/signup with unknown email
    Assert: Status 404, error detail provided.
    """
    # Arrange
    activity_name = "Chess Club"
    email = "unknown@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_nonexistent_activity_returns_404(client):
    """
    Arrange: TestClient ready, activity does not exist.
    Act: DELETE /activities/Nonexistent Activity/signup
    Assert: Status 404, error detail provided.
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_then_signup_same_participant(client):
    """
    Arrange: TestClient ready, participant in activity.
    Act: DELETE, then POST with same email.
    Assert: Participant removed then re-added successfully.
    """
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    
    # Verify participant exists
    response_before = client.get("/activities")
    assert email in response_before.json()[activity_name]["participants"]

    # Act - unregister
    delete_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert unregister worked
    assert delete_response.status_code == 200
    response_after_delete = client.get("/activities")
    assert email not in response_after_delete.json()[activity_name]["participants"]
    
    # Act - signup again
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert signup worked
    assert signup_response.status_code == 200
    response_after_signup = client.get("/activities")
    assert email in response_after_signup.json()[activity_name]["participants"]
