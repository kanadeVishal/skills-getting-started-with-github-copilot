from fastapi.testclient import TestClient
from src.app import app, activities
from urllib.parse import quote


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # We expect activities to be a dict and contain at least 'Chess Club'
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure not already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up via POST (URL-encode activity name)
    encoded = quote(activity, safe='')
    resp = client.post(f"/activities/{encoded}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Unregister via DELETE
    resp = client.delete(f"/activities/{encoded}/participants?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
