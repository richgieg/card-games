from src.uno.events import GameAbandonedEvent, GameStartedEvent
from src.uno.player import Player


def test_get_events(player: Player) -> None:
    player.queue_event(GameStartedEvent(name="game_started"))
    player.queue_event(GameAbandonedEvent(name="game_abandoned"))
    [seq_event1, seq_event2] = player.get_events()
    assert seq_event1["event"]["name"] == "game_started"
    assert seq_event2["event"]["name"] == "game_abandoned"
