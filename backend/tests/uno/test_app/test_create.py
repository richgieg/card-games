from fastapi.testclient import TestClient

from src.uno.constants import MAX_GAMES


def test_create(client: TestClient) -> None:
    response = client.post("/create")
    assert response.json()["error"] is None


def test_create_fails_if_max_games_reached(client: TestClient) -> None:
    for _ in range(0, MAX_GAMES):
        client.post("/create")
    response = client.post("/create")
    assert response.json()["error"] == "max_games_reached"
