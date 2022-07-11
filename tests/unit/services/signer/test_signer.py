from src.services.signer import sign_encoded_state, unsign_state


def test_signer(string_to_sign, secret_key):
    signed_text = sign_encoded_state(string_to_sign, secret_key)
    assert isinstance(signed_text, str)

    unsigned_text = unsign_state(signed_text, secret_key)
    assert string_to_sign == unsigned_text
