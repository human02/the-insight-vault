from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError


def test_health_check(client):
    """Verify the API and DB connection logic are working."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "connected", "database": "PostgresSQL"}


def test_create_link_success(client):
    """Ensure a valid link can be saved."""
    payload = {
        "url": "https://astral.sh",
        "title": "UV Tool",
        "description": "Fast Python manager",
    }
    response = client.post("/links", json=payload)

    assert response.status_code == 201
    assert response.json["url"] == payload["url"]
    assert "id" in response.json


def test_create_link_missing_url(client):
    """Ensure 400 error when URL is missing."""
    payload = {"title": "Missing URL"}
    response = client.post("/links", json=payload)

    assert response.status_code == 400
    assert response.json["error"] == "Bad Request"
    assert response.json["message"] == "URL is required"


def test_global_404_handler(client):
    """Verify that the global error handler catches non-existent routes."""
    response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404
    assert "error" in response.json
    assert response.json["error"] == "Not Found"


def test_create_link_empty_json(client):
    """Verify 400 when sending empty JSON body."""
    response = client.post("/links", json={})
    assert response.status_code == 400
    assert response.json["error"] == "Bad Request"


def test_create_link_empty_payload(client):
    """Test validation when no data is sent."""
    response = client.post("/links", json={})
    assert response.status_code == 400
    assert response.json["error"] == "Bad Request"
    assert response.json["message"] == "URL is required"


def test_method_not_allowed(client):
    """Test 405 error (e.g., trying to GET the /links POST-only route)."""
    # Currently we only defined POST for /links
    response = client.put("/links")
    assert response.status_code == 405
    assert "error" in response.json


def test_get_all_links_success(client):
    """Verify we can retrieve all saved links."""
    # Add a link first
    client.post("/links", json={"url": "https://python.org", "title": "Python"})

    # Retrieve it
    response = client.get("/links")
    assert response.status_code == 200
    assert len(response.json) >= 1
    assert response.json[0]["url"] == "https://python.org"


def test_get_all_links_empty(client):
    """Verify GET works when no links exist."""
    response = client.get("/links")
    assert response.status_code == 200
    assert response.json == []


def test_create_link_db_failure_mock(client):
    """Mock a DB failure to test the 500 error handler."""

    payload = {"url": "https://fail.com"}

    with patch(
        "models.link.db.session.commit", side_effect=SQLAlchemyError("DB Crash")
    ):
        response = client.post("/links", json=payload)
        assert response.status_code == 500
        assert response.json["error"] == "Database Error"

    response = client.get("/links")
    assert response.status_code == 200
