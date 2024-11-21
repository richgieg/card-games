from src.uno.cards import Color, NumberCard
from src.uno.player import Player


def test_add_card(player: Player) -> None:
    player.add_card(NumberCard(0, Color.RED, 0))
    assert len(player.cards) == 1
