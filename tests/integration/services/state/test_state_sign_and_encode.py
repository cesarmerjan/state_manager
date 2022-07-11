from uuid import uuid4

from config import ApiConfig
from src.entities.state import State
from src.services.encoder import decode_state, encode_state
from src.services.signer import sign_encoded_state, unsign_state


def test_state_sign_encode(unit_of_work, Repository):

    state = State({"data": "data"}, str(uuid4()), "service")

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        repository.set(
            state.uuid, sign_encoded_state(encode_state(state), ApiConfig.SECRET_KEY)
        )

        unit_of_work.commit()

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)

        state_claims = repository.get(state.uuid)

        state_claims = decode_state(unsign_state(state_claims, ApiConfig.SECRET_KEY))

    assert state_claims == state.claims
