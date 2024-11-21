from src.uno.constants import GameStatus, MAX_PLAYERS
from src.uno.game import Game


def test_join(game: Game) -> None:
    response = game.join()
    assert response["error"] is None


def test_join_adds_a_player(game: Game) -> None:
    game.join()
    assert len(game.players) == 2


def test_join_queues_event_for_all_players(game: Game) -> None:
    game.join()
    for player in game.players:
        assert len(player.events) == 1
        assert player.events[0]["event"]["name"] == "player_joined"


def test_join_fails_if_game_abandoned(game: Game) -> None:
    game.status = GameStatus.ABANDONED
    response = game.join()
    assert response["error"] == "invalid_status"


def test_join_fails_if_game_finished(game: Game) -> None:
    game.status = GameStatus.FINISHED
    response = game.join()
    assert response["error"] == "invalid_status"


def test_join_fails_if_game_started(game: Game) -> None:
    game.status = GameStatus.FINISHED
    response = game.join()
    assert response["error"] == "invalid_status"


def test_join_fails_if_max_players_reached(game: Game) -> None:
    for _ in range(MAX_PLAYERS - 1):
        game.join()
    response = game.join()
    assert response["error"] == "max_players_reached"
