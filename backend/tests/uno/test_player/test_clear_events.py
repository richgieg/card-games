from src.uno.events import GameStartedEvent
from src.uno.player import Player


def test_clear_events(player: Player) -> None:
    player.queue_event(GameStartedEvent(name="game_started"))
    player.queue_event(GameStartedEvent(name="game_started"))
    player.clear_events()
    assert len(player.events) == 0
