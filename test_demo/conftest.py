import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:5001/api"

@pytest.fixture
def auth_token():
    # create a new unique user
    username = f"user_{int(time.time()*1000)}"
    password = "user123"

    requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": username,
            "password": password
        }
    )

    # login the user
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "username": username,
            "password": password
        }
    )

    # return token
    token = response.json()["access_token"]
    return token