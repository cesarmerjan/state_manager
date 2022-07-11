from uuid import uuid4

from config import ApiConfig
from src.services.signer import sign_encoded_state, unsign_state


def test_signer_with_persistence(unit_of_work, Repository):

    state_data = {"uuid": str(uuid4()), "payload": "data"}

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        repository.set(
            state_data["uuid"],
            sign_encoded_state(state_data["payload"], ApiConfig.SECRET_KEY),
        )
        unit_of_work.commit()

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)

        state = repository.get(state_data["uuid"])

        state_payload = unsign_state(state, ApiConfig.SECRET_KEY)

    assert state_payload == state_data["payload"]
