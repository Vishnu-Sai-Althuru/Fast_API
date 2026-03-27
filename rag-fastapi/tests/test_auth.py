def test_signup(client, unique_username):
    response = client.post("/auth/signup", json={
        "username": unique_username,
        "password": "secret123",
    })
    assert response.status_code == 200


def test_login(client, unique_username):
    client.post("/auth/signup", json={
        "username": unique_username,
        "password": "secret123",
    })

    response = client.post("/auth/login", data={
        "username": unique_username,
        "password": "secret123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()
