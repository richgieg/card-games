from src.uno.cards import Color, NumberCard
from src.uno.player import Player


def test_remove_card(player: Player) -> None:
    card = NumberCard(0, Color.RED, 0)
    player.add_card(card)
    player.remove_card(card)
    assert len(player.cards) == 0
