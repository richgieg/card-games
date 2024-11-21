from src.uno.cards import cards
from src.uno.game import Game


def test_discard_top_card(game: Game) -> None:
    game._discard_top_card()
    assert len(game.discard_pile) == 1
    assert len(game.draw_pile) == len(cards) - 1
