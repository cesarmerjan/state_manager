import json

from src.entities.state import State
from src.services.encoder import decode_state, encode_state


def test_encoder(state_data):
    state = State(**state_data)
    encoded_text = encode_state(state)
    assert isinstance(encoded_text, str)

    decoded_state = decode_state(encoded_text)

    assert state.claims == decoded_state
    assert isinstance(decoded_state, dict)
