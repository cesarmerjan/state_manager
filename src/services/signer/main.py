from string_signer import StringSigner


def sign_encoded_state(encoded_state: str, secret_key: str) -> str:
    signer = StringSigner(secret_key)
    signed_encoded_state = signer.sign(encoded_state)
    return signed_encoded_state


def unsign_state(signed_encoded_state: str, secret_key: str) -> str:
    signer = StringSigner(secret_key)
    unsigned_encoded_state = signer.unsign(signed_encoded_state)
    return unsigned_encoded_state
