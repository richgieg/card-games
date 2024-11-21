from src.uno.cards import Color, NumberCard
from src.uno.player import Player


def test_has_card_of_color_returns_true_if_found(player: Player) -> None:
    player.add_card(NumberCard(0, Color.RED, 0))
    assert player._has_card_of_color(Color.RED)


def test_has_card_of_color_returns_false_if_not_found(player: Player) -> None:
    player.add_card(NumberCard(0, Color.RED, 0))
    assert not player._has_card_of_color(Color.GREEN)
