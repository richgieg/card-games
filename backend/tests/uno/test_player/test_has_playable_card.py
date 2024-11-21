from src.uno.cards import Color, NumberCard
from src.uno.player import Player


def test_has_playable_card_returns_true_when_has_playable_card(player: Player) -> None:
    card = NumberCard(0, Color.RED, 0)
    player.add_card(card)
    discard_pile = [NumberCard(0, Color.RED, 1)]
    assert player.has_playable_card(discard_pile)


def test_has_playable_card_returns_false_when_no_playable_card(player: Player) -> None:
    card = NumberCard(0, Color.YELLOW, 0)
    player.add_card(card)
    discard_pile = [NumberCard(0, Color.RED, 1)]
    assert not player.has_playable_card(discard_pile)
