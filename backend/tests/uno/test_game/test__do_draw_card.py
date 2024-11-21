from src.uno.cards import cards, Color, DiscardedWildCard, WildCard
from src.uno.game import Game


def test_do_draw_card(game: Game) -> None:
    draw_pile_starting_length = len(game.draw_pile)
    game._do_draw_card()
    draw_pile_ending_length = len(game.draw_pile)
    assert draw_pile_ending_length == draw_pile_starting_length - 1


def test_do_draw_card_replenishes_draw_pile(game: Game) -> None:
    for card in game.draw_pile[1:]:
        if isinstance(card, WildCard):
            game.discard_pile.append(
                DiscardedWildCard(Color.GREEN, card))
        else:
            game.discard_pile.append(card)
    game.draw_pile = game.draw_pile[:1]
    last_discard = game.discard_pile[-1]
    game._do_draw_card()
    assert len(game.draw_pile) == len(cards) - 2
    assert len(game.discard_pile) == 1
    assert last_discard is game.discard_pile[-1]
