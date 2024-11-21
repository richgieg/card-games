from src.uno.cards import Action, ActionCard, Color, DiscardedWildCard, NumberCard, WildCard
from src.uno.player import Player


def test_can_play_number_card_on_number_card_with_same_color(player: Player) -> None:
    card = NumberCard(0, Color.BLUE, 0)
    player.add_card(card)
    discard_pile = [NumberCard(0, Color.BLUE, 1)]
    assert player.can_play_card(card, discard_pile)


def test_can_play_number_card_on_number_card_with_same_number(player: Player) -> None:
    card = NumberCard(0, Color.BLUE, 0)
    player.add_card(card)
    discard_pile = [NumberCard(0, Color.RED, 0)]
    assert player.can_play_card(card, discard_pile)


def test_can_play_action_card_on_action_card_with_same_color(player: Player) -> None:
    card = ActionCard(0, Color.RED, Action.DRAW_TWO)
    player.add_card(card)
    discard_pile = [ActionCard(0, Color.RED, Action.REVERSE)]
    assert player.can_play_card(card, discard_pile)


def test_can_play_action_card_on_action_card_with_same_action(player: Player) -> None:
    card = ActionCard(0, Color.RED, Action.SKIP)
    player.add_card(card)
    discard_pile = [ActionCard(0, Color.BLUE, Action.SKIP)]
    assert player.can_play_card(card, discard_pile)


def test_can_play_number_card_on_action_card_with_same_color(player: Player) -> None:
    card = NumberCard(0, Color.RED, 0)
    player.add_card(card)
    discard_pile = [ActionCard(0, Color.RED, Action.SKIP)]
    assert player.can_play_card(card, discard_pile)


def test_can_play_number_card_on_wild_card_with_same_color(player: Player) -> None:
    card = NumberCard(0, Color.RED, 0)
    player.add_card(card)
    discard_pile = [DiscardedWildCard(Color.RED, WildCard(0, False))]
    assert player.can_play_card(card, discard_pile)


def test_can_play_action_card_on_wild_card_with_same_color(player: Player) -> None:
    card = ActionCard(0, Color.RED, Action.SKIP)
    player.add_card(card)
    discard_pile = [DiscardedWildCard(Color.RED, WildCard(0, False))]
    assert player.can_play_card(card, discard_pile)


def test_can_play_wild_card_on_number_card(player: Player) -> None:
    card = WildCard(0, False)
    player.add_card(card)
    discard_pile = [NumberCard(0, Color.BLUE, 1)]
    assert player.can_play_card(card, discard_pile)


def test_can_play_wild_card_on_action_card(player: Player) -> None:
    card = WildCard(0, False)
    player.add_card(card)
    discard_pile = [ActionCard(0, Color.RED, Action.SKIP)]
    assert player.can_play_card(card, discard_pile)


def test_can_play_wild_card_on_wild_card(player: Player) -> None:
    card = WildCard(0, False)
    player.add_card(card)
    discard_pile = [DiscardedWildCard(Color.RED, WildCard(0, False))]
    assert player.can_play_card(card, discard_pile)


def test_can_play_wild_draw_four_card_if_has_no_matching_color_card(player: Player) -> None:
    card = WildCard(0, True)
    player.add_card(card)
    player.add_card(NumberCard(0, Color.RED, 0))
    discard_pile = [ActionCard(0, Color.BLUE, Action.SKIP)]
    assert player.can_play_card(card, discard_pile)


def test_cannot_play_mismatched_number_card_on_number_card(player: Player) -> None:
    card = NumberCard(0, Color.RED, 0)
    player.add_card(card)
    discard_pile = [NumberCard(0, Color.BLUE, 1)]
    assert not player.can_play_card(card, discard_pile)


def test_cannot_play_mismatched_action_card_on_action_card(player: Player) -> None:
    card = ActionCard(0, Color.RED, Action.DRAW_TWO)
    player.add_card(card)
    discard_pile = [ActionCard(0, Color.BLUE, Action.SKIP)]
    assert not player.can_play_card(card, discard_pile)


def test_cannot_play_mismatched_number_card_on_action_card(player: Player) -> None:
    card = NumberCard(0, Color.RED, 0)
    player.add_card(card)
    discard_pile = [ActionCard(0, Color.BLUE, Action.SKIP)]
    assert not player.can_play_card(card, discard_pile)


def test_cannot_play_mismatched_number_card_on_wild_card(player: Player) -> None:
    card = NumberCard(0, Color.RED, 0)
    player.add_card(card)
    discard_pile = [DiscardedWildCard(Color.BLUE, WildCard(0, False))]
    assert not player.can_play_card(card, discard_pile)


def test_cannot_play_mismatched_action_card_on_wild_card(player: Player) -> None:
    card = ActionCard(0, Color.RED, Action.DRAW_TWO)
    player.add_card(card)
    discard_pile = [DiscardedWildCard(Color.BLUE, WildCard(0, False))]
    assert not player.can_play_card(card, discard_pile)


def test_cannot_play_wild_draw_four_card_if_has_matching_color_card(player: Player) -> None:
    card = WildCard(0, True)
    player.add_card(card)
    player.add_card(NumberCard(0, Color.BLUE, 0))
    discard_pile = [ActionCard(0, Color.BLUE, Action.SKIP)]
    assert not player.can_play_card(card, discard_pile)
