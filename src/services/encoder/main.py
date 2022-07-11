import json

from web_encoder import WebEncoder

from src.entities.state import State


def encode_state(state: State) -> str:
    web_encoder = WebEncoder()
    encoded_state = web_encoder.encode(json.dumps(state.claims))
    return encoded_state


def decode_state(encoded_state: str) -> dict:
    web_encoder = WebEncoder()
    state = json.loads(web_encoder.decode(encoded_state))
    return state
