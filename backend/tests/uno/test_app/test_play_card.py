from fastapi.testclient import TestClient


def test_play_card_fails_if_game_not_found(client: TestClient) -> None:
    response = client.post(
        "/play-card", params={"game_id": "bad_game_id", "player_id": "some_player_id", "card_id": 0})
    assert response.json()["error"] == "game_not_found"
