
def test_register_returns_token_and_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "student2",
            "email": "student2@example.com",
            "class_name": "12SD",
            "password": "Password123",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token"]
    assert body["user"]["username"] == "student2"
    assert body["user"]["class_name"] == "12SD"


def test_register_rejects_invalid_class_branch(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "student3",
            "email": "student3@example.com",
            "class_name": "BAD",
            "password": "Password123",
        },
    )
    assert response.status_code == 400


def test_register_rejects_duplicate_username_branch(client, registered_user):
    response = client.post(
        "/auth/register",
        json={
            "username": "student1",
            "email": "new@example.com",
            "class_name": "12SV",
            "password": "Password123",
        },
    )
    assert response.status_code == 400


def test_login_success_and_me(client, registered_user):
    login = client.post(
        "/auth/login",
        json={"username": "student1", "password": "Password123"},
    )
    assert login.status_code == 200
    token = login.json()["token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == "student1"


def test_login_rejects_wrong_password_branch(client, registered_user):
    response = client.post(
        "/auth/login",
        json={"username": "student1", "password": "WrongPassword"},
    )
    assert response.status_code == 401
