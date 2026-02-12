def test_health_check(client):
    """Verify the API and DB connection logic are working."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "connected", "database": "PostgresSQL"}
