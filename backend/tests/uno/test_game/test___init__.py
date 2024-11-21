from src.uno.cards import cards
from src.uno.constants import GameStatus
from src.uno.game import Game


def test_init(game: Game) -> None:
    assert game.status == GameStatus.CREATED
    assert len(game.players) == 1
    assert len(game.draw_pile) == len(cards)
    assert game.draw_pile is not cards
    assert len(game.discard_pile) == 0
    assert game.active_player_index == 0
    assert game.reversed == False
