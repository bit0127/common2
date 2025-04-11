"""
Authentication module.

This module contains functions to create and decode JWT tokens, hash passwords,
and verify passwords.

"""

import os
import datetime
import jwt
import boto3
from chalice import BadRequestError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_secret_key():
    """Fetch the JWT secret key from AWS Secrets Manager."""
    jwt_secret_key_name = os.getenv("JWT_SECRET_KEY_NAME")
    session = boto3.session.Session()
    secrets_manager_client = session.client(
        service_name="secretsmanager", region_name=os.getenv("SECRET_REGION")
    )

    try:
        get_secret_value_response = secrets_manager_client.get_secret_value(
            SecretId=jwt_secret_key_name
        )
        secret = get_secret_value_response["SecretString"]
        return secret
    except Exception as e:
        raise BadRequestError(f"Failed to retrieve secret key: {str(e)}") from e


def create_jwt(user_id):
    """Create JWT token."""
    secret_key = get_secret_key()
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {"user_id": user_id, "exp": expiration}
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def decode_jwt(token):
    """Decode JWT token."""
    secret_key = get_secret_key()

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise BadRequestError("Token has expired") from e
    except jwt.InvalidTokenError as e:
        raise BadRequestError("Invalid token") from e


def hash_password(password: str) -> str:
    """Hashes a password before storing it in DynamoDB"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the provided password matches the stored hash"""
    return pwd_context.verify(plain_password, hashed_password)
