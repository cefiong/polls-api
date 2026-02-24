import pytest
import requests
import time
from tests.conftest import BASE_URL

def test_health_check():
    """ Test that the health enpoint returns healthy status"""
    # Make a request to health endpoint

    response = requests.get(f"{BASE_URL}/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"


def test_register_user():
    """Test user registration"""
    user_data = {
        "username": f"testuser_{int(time.time() * 1000)}",
        "password": "testpass123"
    }

    # Register user
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=user_data
    )

    # Check response
    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert "user" in data
    assert data["user"]["username"] == user_data["username"]

def test_create_poll(auth_token):
    """Test creating a public poll"""
    # Arrange: Poll data
    poll_data = {
        "question": "What is your favorite language?",
        "options": ["Python", "JavaScript", "Java"],
        "is_public": True,
        "requires_admin": False
    }

    # Act: Create poll
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(
        f"{BASE_URL}/polls",
        json=poll_data,
        headers=headers
    )

    # Assert: Check response
    assert response.status_code == 201
    data = response.json()
    assert data["question"] == poll_data["question"]
    assert data["is_public"] == True
    assert len(data["options"]) == 3
    assert "id" in data


def test_vote_on_poll(auth_token):
    """Test voting on a public poll"""
    # Arrange: Create a poll first
    poll_data = {
        "question": "Favorite color?",
        "options": ["Red", "Blue", "Green"],
        "is_public": True
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = requests.post(
        f"{BASE_URL}/polls",
        json=poll_data,
        headers=headers
    )
    poll_id = create_response.json()["id"]

    # Act: Vote
    vote_data = {"choice": "Red"}
    response = requests.post(
        f"{BASE_URL}/votes/poll/{poll_id}",
        json=vote_data
    )

    # Assert: Check response
    assert response.status_code == 201
    data = response.json()
    assert data["poll_id"] == poll_id
    assert data["choice"] == "Red"