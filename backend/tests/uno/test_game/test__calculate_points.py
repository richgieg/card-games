from src.uno.cards import Action, ActionCard, Color, NumberCard, WildCard
from src.uno.constants import ACTION_CARD_POINTS, WILD_CARD_POINTS
from src.uno.game import Game


def test_calculate_points(game: Game) -> None:
    game.join()
    game.join()
    game.players[0].cards = [NumberCard(0, Color.RED, 5)]
    game.players[1].cards = [
        ActionCard(0, Color.GREEN, Action.DRAW_TWO),
        ActionCard(0, Color.BLUE, Action.REVERSE)
    ]
    game.players[2].cards = [
        WildCard(0, True),
        WildCard(0, False),
        NumberCard(0, Color.BLUE, 9)
    ]
    expected_points = 2 * ACTION_CARD_POINTS + 2 * WILD_CARD_POINTS + 5 + 9
    assert game._calculate_points() == expected_points
