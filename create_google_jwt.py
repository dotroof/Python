import json
import time

import jwt

if __name__ == "__main__":

    service_json_dict = open("./service.json", "r")
    service_json = json.load(service_json_dict)

    headers = {
        "alg": "RS256",
        "typ": "JWT"
    }

    iat = time.time()
    exp = iat + 3600
    payload = {
        "iss": service_json["client_email"],
        "scope": "https://www.googleapis.com/auth/androidpublisher",
        "aud": "https://oauth2.googleapis.com/token",
        "exp": exp,
        "iat": iat
    }

    token = jwt.encode(payload, service_json["private_key"], algorithm="RS256", headers=headers)

    print("jwt: ", token)
