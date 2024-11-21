from fastapi.testclient import TestClient


def test_get_state_fails_if_game_not_found(client: TestClient) -> None:
    response = client.get(
        "/get-state", params={"game_id": "bad_game_id", "player_id": "some_player_id"})
    assert response.json()["error"] == "game_not_found"
