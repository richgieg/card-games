from src.uno.constants import CARDS_PER_PLAYER
from src.uno.game import Game


def test_deal_cards_to_players(game: Game) -> None:
    draw_pile_starting_length = len(game.draw_pile)
    game.join()
    game._deal_cards_to_players()
    assert len(game.players[0].cards) == CARDS_PER_PLAYER
    assert len(game.players[1].cards) == CARDS_PER_PLAYER
    draw_pile_ending_length = len(game.draw_pile)
    assert draw_pile_ending_length == draw_pile_starting_length - \
        (2 * CARDS_PER_PLAYER)
