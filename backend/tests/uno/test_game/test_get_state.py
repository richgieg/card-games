from src.uno.game import Game


def test_get_state(game: Game) -> None:
    player_id = game.players[0].id
    response = game.get_state(player_id)
    assert response["error"] is None


def test_get_state_clears_player_events(game: Game) -> None:
    player_id = game.players[0].id
    game.get_state(player_id)
    assert len(game.players[0].events) == 0


def test_get_state_fails_if_player_not_found(game: Game) -> None:
    response = game.get_state("bad_player_id")
    assert response["error"] == "player_not_found"
