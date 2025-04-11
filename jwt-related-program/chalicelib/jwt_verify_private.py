import jwt
from urllib.request import urlopen
import base64

# TXT_FILE_PATH = os.path.join(os.path.dirname(__file__), 'chalicelib', 'jwt-txt.text')

PUBLIC_KEY_PEM = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtv5yWUn9w2K1hIrEEkyg
zvdZJG7bPuPMO80sMskRyu1yOh25Tk/Mcwmfxkuy3+HyPnBIi6G29e9crvxlo1qY
jvhmtvuqVJkwnhhXTyRhQZ7No2LLgM18BoSBBci8mrCxiHvyhVx1asdcXAZYyT3X
paRUMgi9xeUoOIFDutIOBXPJWJjvhOeuH2KsYCLKxIuayyMlIuX2x21oSQ3CpNiG
8o3QM6WU7IrIFypFAe9Kt5WqFt3S9+BlLsGy2Gf49y7UMNUpoijuDAyX09cyus/X
aVM6eacFHMEgqk9N9cjiflx8D5XuZ2oEZdsCLxC8fB8D43LP0yXO3xdEjw9mAbOi
KQIDAQAB
-----END PUBLIC KEY-----
"""
def decode_base64_url(data):
    data += '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data).decode('utf-8')

def jwt_private_key23():
    try:
        with urlopen("https://cdn.kibe.la/media/shared/12170/22c8d20e-af7b-40cd-a1cb-be32eeb8d866/38905/attachment.txt?_gl=1*1wjci3w*_gcl_au*MTIxNTc0NDA5MS4xNzM3NTQyNjQw") as response:
            jwt_list = response.read().decode('utf-8').strip().splitlines()
            # print(jwt_list)
    except Exception as e:
        return {"error": f"Failed to read the file from URL: {str(e)}"}

    for token in jwt_list:
        token = token.strip()
        try:
            header, payload, signature = token.split('.')
            # decoded_payload = decode_base64_url(payload)
            # print("Payload:", json.loads(decoded_payload))

            decoded = jwt.decode(token, PUBLIC_KEY_PEM, algorithms=["PS256"])
            print(decoded)
            
        except jwt.InvalidTokenError:
            continue