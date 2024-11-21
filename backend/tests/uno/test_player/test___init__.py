from src.uno.player import Player


def test___init__(player: Player) -> None:
    assert len(player.cards) == 0
    assert len(player.events) == 0
    assert player.next_event_id == 0
    assert player.rounds_won == 0
    assert player.points == 0
