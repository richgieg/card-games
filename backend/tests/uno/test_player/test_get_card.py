from src.uno.cards import Color, NumberCard
from src.uno.player import Player


def test_get_card_returns_card_if_found(player: Player) -> None:
    card_id = 0
    player.add_card(NumberCard(card_id, Color.RED, 0))
    assert player.get_card(card_id) is not None


def test_get_card_returns_none_if_not_found(player: Player) -> None:
    card_id = 0
    player.add_card(NumberCard(card_id, Color.RED, 0))
    assert player.get_card(1) is None
