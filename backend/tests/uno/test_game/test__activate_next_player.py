from src.uno.game import Game


def test_activate_next_player(game: Game) -> None:
    game.join()
    game._activate_next_player()
    assert game.active_player_index == 1


def test_activate_next_player_wraps_around(game: Game) -> None:
    game.join()
    game._activate_next_player()
    game._activate_next_player()
    assert game.active_player_index == 0


def test_activate_next_player_in_reverse(game: Game) -> None:
    game.join()
    game._activate_next_player()
    game.reversed = True
    game._activate_next_player()
    assert game.active_player_index == 0


def test_activate_next_player_wraps_around_in_reverse(game: Game) -> None:
    game.join()
    game.reversed = True
    game._activate_next_player()
    assert game.active_player_index == 1
