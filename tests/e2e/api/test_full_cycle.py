def test_post_state(api_client, api_header_with_key, session_cookie_name):

    state_data = {
        "payload": {
            "authentication": "LOGGED",
            "permissions": ["add_user", "delete_user"],
        },
        "subject": "1730b54d-5842-4675-a1f9-0d6fe0703557",
        "timeToExpire": {"seconds": 45, "minutes": 15, "hours": 2, "days": 1},
    }

    response = api_client.post("/state/", headers=api_header_with_key, json=state_data)

    assert response.status_code == 201

    session_cookie = {}
    for cookie in response.cookies:
        if cookie.name == session_cookie_name:
            session_cookie = {cookie.name: cookie.value}

    assert session_cookie

    response = api_client.get(
        "/state/status", headers=api_header_with_key, cookies=session_cookie
    )

    assert response.status_code == 200

    response = api_client.get(
        "/state/", headers=api_header_with_key, cookies=session_cookie
    )

    assert response.json()["payload"] == state_data["payload"]
    assert response.json()["subject"] == state_data["subject"]
    assert response.json()["issuer"] == "testclient"
    assert response.json()["audience"] == ["*"]

    response = api_client.delete(
        "/state/", headers=api_header_with_key, cookies=session_cookie
    )

    assert not response.cookies.get(session_cookie_name)
    assert response.status_code == 202
