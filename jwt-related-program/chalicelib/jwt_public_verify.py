import jwt
import os
from urllib.request import urlopen
import base64

# TXT_FILE_PATH = os.path.join(os.path.dirname(__file__), 'chalicelib', 'jwt-txt.text')

PUBLIC_KEY_PEM = """
-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAuniw7mDOEyiCkb3OTEgjxojEouz2JmzzAJF+kGzXNz2bZbw4yC/W
WFbK1YMOxSL86cM6Lqk1eiuNNQHEYe49uAF8TWh9znguLssfLtbtJn8VAegwehY3
42bA+OrqkL4+vxsGRiz5GfBsnbqm4u++j2/S7gRMmaOsCBo0LB2xCyZqLuHtkngR
FOshejIhUPgxitsZer4pI7JWM8F0go+6Q9oaFQHOZ0ucI1OXH+q3qwwXGJr45De6
rwTPiZElKFkYy228qqCSSB0UB0GWsuhxTnPPMAmPih8Jz4O/kFkzTKUIBQwUNEa2
p9TJvyx+hyu39Jk/A5ffcwgSP+gTCslQOQIDAQAB
-----END RSA PUBLIC KEY-----
"""
def decode_base64_url(data):
    data += '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data).decode('utf-8')

def jwt_public_key21():
    try:
        with urlopen("https://cdn.kibe.la/media/shared/12170/22c8d20e-af7b-40cd-a1cb-be32eeb8d866/27560/attachment.txt?_gl=1*1ofpj3h*_gcl_au*MTIxNTc0NDA5MS4xNzM3NTQyNjQw") as response:
            jwt_list = response.read().decode('utf-8').strip().splitlines()
    except Exception as e:
        return {"error": f"Failed to read the file from URL: {str(e)}"}

    for token in jwt_list:
        token = token.strip()
        try:
            header, payload, signature = token.split('.')
            decoded_payload = decode_base64_url(payload)
            # print("Payload:", json.loads(decoded_payload))

            decoded = jwt.decode(token, PUBLIC_KEY_PEM, algorithms=["RS256"])
            print(decoded)
        except jwt.InvalidTokenError:
            continue