from fastapi.testclient import TestClient
from app.main import app
import pytest


client = TestClient(app)

expected_res = [
        {
            "username": "Snake",
            "user_type": "Admin",
            "organization_name": "Metal Gear Solid",
            "organization_tier": "Enterprise"
        },
        {
            "username": "Ocelot",
            "user_type": "User",
            "organization_name": "Metal Gear Solid 5",
            "organization_tier": "Medium"
        },
        {
            "username": "Peach",
            "user_type": "Creator",
            "organization_name": "Super Mario",
            "organization_tier": "Medium"
        },
        {
            "username": "Freeman",
            "user_type": "Admin",
            "organization_name": "Half Life",
            "organization_tier": "Medium"
        },
        {
            "username": "Athena",
            "user_type": "Creator",
            "organization_name": "God of War",
            "organization_tier": "Medium"
        }
]

@pytest.mark.parametrize("username, user_last_state", [
    ("Snake", expected_res[0]),
    ("Ocelot", expected_res[1]),
    ("Peach", expected_res[2]),
    ("Freeman", expected_res[3]),
    ("Athena", expected_res[4])
])
def test_get_user_last_state_good_username(username, user_last_state):
    response = client.get(f"/api/users/{username}")
    assert response.status_code == 200
    assert response.json() == user_last_state


def test_user_not_found():
    response = client.get("/api/users/fake_user")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }


def test_no_username_provided():
    response = client.get("/api/users/")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found"
    }