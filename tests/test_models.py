import pytest
from models import User

def test_user_password_hashing():
    """Test that password hashing and checking works correctly"""

    # Create a user
    user = User(username="testuser")
    user.set_password("password123")

    # Check for correct password
    assert user.check_password("password123") is True

    # Check for incorrect password
    assert user.check_password("wrongpassword") is False

    # Check that password is not stored as plain text
    assert user.password_hash != "password123"
