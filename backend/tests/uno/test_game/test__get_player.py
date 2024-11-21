from src.uno.game import Game


def test_get_player_returns_player_if_found(game: Game) -> None:
    player_id = game.players[0].id
    player = game._get_player(player_id)
    assert player is not None


def test_get_player_returns_none_if_player_not_found(game: Game) -> None:
    player = game._get_player("bad_player_id")
    assert player is None
