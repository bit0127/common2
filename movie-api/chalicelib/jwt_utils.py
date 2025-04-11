import jwt
import os
import boto3
from datetime import datetime, timedelta


# Get the secret key from the environment variables, although it is best to use secret manager
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
secrets_client = boto3.client("secretsmanager")

# Function to encode JWT
def encode_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def decode_jwt(token):
    try:
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
