from src.uno.game import Game


def test_player_is_admin_returns_true_if_admin(game: Game) -> None:
    player1 = game.players[0]
    assert game._player_is_admin(player1)


def test_player_is_admin_returns_false_if_not_admin(game: Game) -> None:
    game.join()
    player2 = game.players[1]
    assert not game._player_is_admin(player2)
