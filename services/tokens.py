import hashlib


def generate_token(data: str, salt: str, length: int = -1, iterations: int = 1000):
    data = data.encode("utf-8")
    salt = salt.encode("utf-8")

    token = hashlib.pbkdf2_hmac("sha256", data, salt, iterations).hex()

    if length != -1:
        token = token[:length]

    return token
