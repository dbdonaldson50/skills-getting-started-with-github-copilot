import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("participants" in v for v in data.values())


def test_signup_and_unregister():
    # Use a known activity
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser@example.com"

    # Ensure not already registered
    client.delete(f"/activities/{activity}/unregister?email={email}")

    # Sign up
    resp_signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_signup.status_code == 200
    assert f"Signed up {email}" in resp_signup.json()["message"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_unreg = client.delete(
        f"/activities/{activity}/unregister?email={email}")
    assert resp_unreg.status_code == 200
    assert f"Unregistered {email}" in resp_unreg.json()["message"]

    # Unregister again should fail
    resp_unreg2 = client.delete(
        f"/activities/{activity}/unregister?email={email}")
    assert resp_unreg2.status_code == 400
