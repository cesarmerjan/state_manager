from uuid import uuid4

from src.entities.state import State
from src.services.encoder import decode_state, encode_state


def test_encoder_with_persistence(unit_of_work, Repository):

    state = State({"data": "data"}, str(uuid4()), "service")

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        repository.set(state.uuid, encode_state(state))
        unit_of_work.commit()

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        state_claims = repository.get(state.uuid)

        state_claims = decode_state(state_claims)

    assert state_claims == state.claims
