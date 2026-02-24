import pytest
import requests
from models import User
import time
from test_demo.conftest import BASE_URL

def test_user_model():
    user = User(username="jdoe")
    user.set_password("jdoe123")

    # test that password is correct
    assert user.check_password("jdoe123") is True
    # test if possword is wrong
    assert user.check_password("wrong_joe123") is False
    # test that password is hashed
    assert user.password_hash != "jdoe123"
    assert user.password_hash is not None

def test_user_registration():
    user_data = {
        "username": f"jdoe_{int(time.time() * 1000)}",
        "password": "jdoe123"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)

    assert response.status_code == 201
    data = response.json()

    assert data["user"]["username"] == user_data["username"]
    assert "message" in data


def test_create_poll(auth_token):
    poll_data = {
        "question": "What is your favorite programming language?",
        "options": [
            "Python",
            "JavaScript",
            "Java",
            "C++"
        ],
        "is_public": True,
        "requires_admin": False
    }
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.post(
        f"{BASE_URL}/polls",
        json=poll_data,
        headers=headers
    )

    print(response.json())
