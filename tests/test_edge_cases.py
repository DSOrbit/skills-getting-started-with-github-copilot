"""
Tests for edge cases and boundary conditions.
Follows AAA pattern: Arrange, Act, Assert.
"""

import pytest


def test_duplicate_signup_rejected(client):
    """
    Arrange: TestClient ready, participant already in activity.
    Act: POST signup for same email twice.
    Assert: First signup succeeds, second is rejected with 400.
    Note: This documents current behavior - duplicates are prevented.
    """
    # Arrange
    activity_name = "Chess Club"
    email = "test.duplicate@mergington.edu"
    
    # Act - first signup
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Act - second signup with same email
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert - first succeeds, second is rejected
    assert response1.status_code == 200
    assert response2.status_code == 400
    
    # Verify only one instance is in participants
    response_get = client.get("/activities")
    participants = response_get.json()[activity_name]["participants"]
    assert participants.count(email) == 1


def test_signup_capacity_not_enforced(client):
    """
    Arrange: TestClient ready, activity with max_participants = 12.
    Act: Try to signup beyond capacity.
    Assert: Signup still succeeds (capacity not enforced currently).
    Note: This documents current behavior; capacity check could be added later.
    """
    # Arrange
    activity_name = "Chess Club"  # max_participants = 12, currently has 2
    
    # Generate new emails for signup attempts
    new_emails = [f"capacity.test{i}@mergington.edu" for i in range(15)]
    
    # Act & Assert - sign up 15 new participants (total would be 17)
    for email in new_emails:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify all were added despite exceeding max_participants
    response_get = client.get("/activities")
    participants = response_get.json()[activity_name]["participants"]
    assert len(participants) == 17  # 2 initial + 15 new


def test_special_characters_in_email(client):
    """
    Arrange: TestClient ready, email with special characters prepared.
    Act: POST signup with special character email.
    Assert: Signup accepted and stored correctly.
    """
    # Arrange
    activity_name = "Programming Class"
    email = "test+special@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    response_get = client.get("/activities")
    assert email in response_get.json()[activity_name]["participants"]


def test_url_encoded_activity_name(client):
    """
    Arrange: TestClient ready, activity name with spaces (URL encoded).
    Act: POST signup with URL-encoded activity name.
    Assert: Signup works with proper encoding.
    """
    # Arrange
    activity_name = "Programming Class"
    email = "url.test@mergington.edu"
    
    # Act - activity name with spaces needs to be part of URL
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    response_get = client.get("/activities")
    assert email in response_get.json()[activity_name]["participants"]


def test_root_redirect(client):
    """
    Arrange: TestClient ready.
    Act: GET /
    Assert: Redirects to /static/index.html
    """
    # Arrange - implicit via fixture
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307  # or 308 depending on redirect type
    assert "/static/index.html" in response.headers.get("location", "")


def test_test_isolation_between_runs(client):
    """
    Arrange: TestClient ready for first test.
    Act: Add participant, fixture resets, new client created.
    Assert: New client sees clean state (no spillover from previous test).
    Note: This test should be run after a test that modifies state.
    """
    # Arrange
    activity_name = "Chess Club"
    
    # Act & Assert - should see original participants (2), not any added in other tests
    response = client.get("/activities")
    participants = response.json()[activity_name]["participants"]
    
    # Original state should have exactly 2
    assert participants.count("michael@mergington.edu") == 1
    assert participants.count("daniel@mergington.edu") == 1
    assert len(participants) == 2
