from src.uno.events import GameStartedEvent
from src.uno.game import Game


def test_get_events(game: Game) -> None:
    player = game.players[0]
    player.queue_event(GameStartedEvent(name="game_started"))
    response = game.get_events(player.id)
    assert response["error"] is None
    assert len(response["events"]) == 1


def test_get_events_clears_player_events(game: Game) -> None:
    player = game.players[0]
    player.queue_event(GameStartedEvent(name="game_started"))
    game.get_events(player.id)
    assert len(player.events) == 0


def test_get_events_fails_if_player_not_found(game: Game) -> None:
    response = game.get_events("bad_player_id")
    assert response["error"] == "player_not_found"
