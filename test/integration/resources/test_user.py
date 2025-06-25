import datetime
from flask_jwt_extended import create_access_token

from app.models import UserModel


# test create user
def test_register_user_creates_account(client):
    response = client.post("/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    assert response.json["message"] == "User created successfully."


# test duplicate username
def test_register_duplicate_user_returns_409(client, session):
    client.post("/register", json={"username": "dupuser", "password": "pass123"})
    response = client.post("/register", json={"username": "dupuser", "password": "another"})
    assert response.status_code == 409
    assert "already exists" in response.json["message"]


# test invalid payload
def test_register_missing_fields_returns_422(client):
    response = client.post("/register", json={})
    assert response.status_code == 422
    assert "username" in response.json["errors"]["json"]
    assert "password" in response.json["errors"]["json"]


## /register-admin

# test create admin
def test_register_admin_creates_admin_account(client):
    response = client.post("/register-admin", json={"username": "admin", "password": "adminpass"})
    assert response.status_code == 201
    assert response.json["message"] == "Admin created successfully."


# test duplicate admin
def test_register_duplicate_admin_returns_409(client):
    client.post("/register-admin", json={"username": "admin", "password": "adminpass"})
    response = client.post("/register-admin", json={"username": "admin", "password": "another"})
    assert response.status_code == 409


# test invalid payload
def test_register_admin_missing_fields_returns_422(client):
    response = client.post("/register-admin", json={})
    assert response.status_code == 422
    assert "username" in response.json["errors"]["json"]
    assert "password" in response.json["errors"]["json"]


## /login

# test valid credential
def test_login_valid_credentials_returns_token(client):
    client.post("/register", json={"username": "loginuser", "password": "secret"})
    response = client.post("/login", json={"username": "loginuser", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json


# test invalid credential
def test_login_invalid_credentials_returns_401(client):
    response = client.post("/login", json={"username": "nouser", "password": "wrong"})
    assert response.status_code == 401
    assert "Invalid credentials." in response.json["message"]


# test invalid payload
def test_log_in_missing_fields_returns_422(client):
    response = client.post("/login", json={})
    assert response.status_code == 422
    assert "username" in response.json["errors"]["json"]
    assert "password" in response.json["errors"]["json"]


## logout

# test log out
def test_logout_successful(client, auth_header):
    response = client.post("/logout", headers=auth_header)
    assert response.status_code == 200
    assert response.json["message"] == "Successfully logged out"


# test token reuse after logout
def test_token_reuse_after_logout_is_blocked(client, auth_header):
    logout_response = client.post("/logout", headers=auth_header)
    assert logout_response.status_code == 200

    
    protected_response = client.get("/user/1", headers=auth_header)
    assert protected_response.status_code == 401
    assert "Token has been revoked" in protected_response.json["msg"]


## /user/<user_id>

# test get user by id
def test_get_user_by_admin_returns_user(client, session, admin_auth_header):
    from app.models import UserModel
    user = UserModel(username="someuser", password="testpass")
    session.add(user)
    session.commit()

    response = client.get(f"/user/{user.user_id}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json["username"] == "someuser"


# test requires admin
def test_get_user_requires_admin_returns_401(client, auth_header):
    response = client.get("/user/1", headers=auth_header)
    assert response.status_code == 401
    assert "Admin privilege required." in response.json["message"]


# test delete
def test_delete_user_by_admin(client, session, admin_auth_header):
    from app.models import UserModel
    user = UserModel(username="tobedeleted", password="secret")
    session.add(user)
    session.commit()

    response = client.delete(f"/user/{user.user_id}", headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json["message"] == "User deleted."


# test requires admin
def test_delete_user_requires_admin_returns_401(client, auth_header):
    response = client.delete("/user/1", headers=auth_header)
    assert response.status_code == 401
    assert "Admin privilege required." in response.json["message"]


## JWT
# test expired token
def test_expired_token(client, session, monkeypatch):
    # Setup
    user = UserModel(username="expireduser", password="pass")
    session.add(user)
    session.commit()

    access_token = create_access_token(
        identity=str(user.user_id),
        expires_delta=datetime.timedelta(seconds=-1)  # already expired
    )
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/user/1", headers=headers)
    assert response.status_code == 401
    assert response.json["error"] == "token_expired"
    assert response.json["description"] == "The token has expired."


# invalid token
def test_invalid_token_returns_401(client):
    headers = {"Authorization": "Bearer not.a.valid.token"}
    response = client.get("/user/1", headers=headers)

    assert response.status_code == 401
    assert response.json["error"] == "invalid_token"
    assert response.json["description"] == "Signature verification failed."


# authorisation required
def test_post_required_auth(client):
    response = client.post("/store", json={"store_name": "Store"})
    assert response.status_code == 401
    assert response.json["description"] == "Request does not contain an access token."
    assert response.json["error"] == "authorization_required"
