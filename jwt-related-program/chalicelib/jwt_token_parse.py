import base64
import json


def jwt_got_flag():

    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmbGFnIjoiZjFuYXQzeHRoZHs4MDExODE0Yi00NzBjLTRmM2MtYWE2ZS0yMTVhYThkYjk5MjR9In0.-LoKWOcI9J1xbnul1YziIxjUziIIS8jZMfpB1HPx4BI"
    header_encoded, payload_encoded, signature = jwt_token.split(".")

    padding = '=' * (4 - len(payload_encoded) % 4)
    payload_decoded = base64.urlsafe_b64decode(payload_encoded + padding).decode("utf-8")

    payload = json.loads(payload_decoded)

    flag = payload.get("flag")

    print("Flag:", flag)
