import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Check participant added
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    # Check participant removed
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]

def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    activity = "Programming Class"
    # Sign up first time
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Sign up again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={email}")

def test_unregister_not_signed_up():
    email = "notregistered@mergington.edu"
    activity = "Art Studio"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
