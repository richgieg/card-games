from src.uno.events import GameStartedEvent
from src.uno.game import Game


def test_queue_event_for_all_players(game: Game) -> None:
    player1 = game.players[0]
    game.join()
    player2 = game.players[1]
    player1.clear_events()
    player2.clear_events()
    game._queue_event_for_all_players(GameStartedEvent(name="game_started"))
    [player1_seq_event] = player1.get_events()
    [player2_seq_event] = player2.get_events()
    assert player1_seq_event["event"]["name"] == "game_started"
    assert player2_seq_event["event"]["name"] == "game_started"
