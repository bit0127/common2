import jwt
import os
import boto3
from datetime import datetime, timedelta


JWT_SECRET_KEY_NAME = os.getenv('JWT_SECRET_KEY_NAME')
secrets_client = boto3.client("secretsmanager")

def get_jwt_secret():
    try:
        response = secrets_client.get_secret_value(SecretId=JWT_SECRET_KEY_NAME)
        if "SecretString" in response:
            return response["SecretString"]
        else:
            print("may be it is not string")
    except ValueError:
        return None

def encode_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    JWT_SECRET_KEY = get_jwt_secret()
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def decode_jwt(token):
    try:
        JWT_SECRET_KEY = get_jwt_secret()
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def verify_jwt(token):
    try:
        user_id = decode_jwt(token)
        return user_id
    except ValueError:
        return None
