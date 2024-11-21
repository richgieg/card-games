from src.uno.events import GameStartedEvent
from src.uno.player import Player


def test_queue_event(player: Player) -> None:
    player.queue_event(GameStartedEvent(name="game_started"))
    player.queue_event(GameStartedEvent(name="game_started"))
    assert len(player.events) == 2
    assert player.next_event_id == 2
    [seq_event1, seq_event2] = player.get_events()
    assert seq_event1["id"] == 0
    assert seq_event2["id"] == 1
