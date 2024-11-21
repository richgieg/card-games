from fastapi.testclient import TestClient


def test_join_fails_if_game_not_found(client: TestClient) -> None:
    response = client.post("/join", params={"game_id": "bad_game_id"})
    assert response.json()["error"] == "game_not_found"
