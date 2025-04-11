import pytest
import time
from chalicelib.jwt_utils import encode_jwt, decode_jwt

SECRET_KEY = "your-very-secret-key"

def test_jwt_token():
    user_id = "user1"
    token = encode_jwt(user_id)
    decoded = decode_jwt(token)

    assert decoded["user_id"] == user_id
    assert "exp" in decoded

def test_jwt_expiry():
    user_id = "user1"
    token = encode_jwt(user_id, expiry_seconds=2)  # Token expires in 2 seconds
    time.sleep(3)  # Wait for token to expire

    with pytest.raises(Exception):
        decode_jwt(token)  # This should raise an error due to expiration