"""
This is test file for auth.py file.
 It contains test cases for create_jwt, decode_jwt, hash_password and verify_password functions.
"""

import sys
import os
from unittest.mock import patch
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from chalicelib.auth import create_jwt, decode_jwt, hash_password, verify_password


@pytest.fixture
def mock_secret_key():
    """Mock the get_secret_key function to return a dummy secret."""
    with patch("chalicelib.auth.get_secret_key", return_value="mocked_secret"):
        yield


@pytest.mark.usefixtures("mock_secret_key")
def test_create_jwt():
    """Test JWT token creation."""
    user_id = "test-user-id"
    token = create_jwt(user_id)
    assert isinstance(token, str)


@pytest.mark.usefixtures("mock_secret_key")
def test_decode_jwt():
    """Test JWT decoding."""
    user_id = "test-user-id"
    token = create_jwt(user_id)
    decoded = decode_jwt(token)
    assert decoded["user_id"] == user_id


def test_hash_and_verify_password():
    """Test password hashing and verification."""
    password = "securepassword"
    hashed = hash_password(password)
    assert hashed != password

    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)
