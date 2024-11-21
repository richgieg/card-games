from src.uno.cards import Color, NumberCard
from src.uno.constants import GameStatus
from src.uno.game import Game


def test_draw_card(game: Game) -> None:
    game.join()
    player1_id = game.players[0].id
    game.start(player1_id)
    game.players[0].cards = []  # Ensure there is no playable card
    top_card = game.draw_pile[-1]
    response = game.draw_card(player1_id)
    assert response["error"] is None
    assert len(game.players[0].cards) == 1
    assert game.players[0].cards[0] == top_card


def test_draw_card_activates_next_player_if_card_not_playable(game: Game) -> None:
    game.join()
    player1_id = game.players[0].id
    game.start(player1_id)
    game.players[0].cards = []  # Ensure there is no playable card
    game.discard_pile.append(NumberCard(0, Color.RED, 0))
    game.draw_pile.append(NumberCard(0, Color.YELLOW, 1))
    game.draw_card(player1_id)
    assert game.active_player_index == 1


def test_draw_card_clears_player_events(game: Game) -> None:
    game.join()
    player1_id = game.players[0].id
    game.start(player1_id)
    game.players[0].cards = []  # Ensure there is no playable card
    game.draw_card(player1_id)
    assert len(game.players[0].events) == 0


def test_draw_card_does_not_activate_next_player_if_card_playable(game: Game) -> None:
    game.join()
    player1_id = game.players[0].id
    game.start(player1_id)
    game.players[0].cards = []  # Ensure there is no playable card
    game.discard_pile.append(NumberCard(0, Color.RED, 0))
    game.draw_pile.append(NumberCard(0, Color.RED, 1))
    game.draw_card(player1_id)
    assert game.active_player_index == 0


def test_draw_card_queues_player_activated_event_if_card_not_playable(game: Game) -> None:
    game.join()
    player1_id = game.players[0].id
    player1_pid = game.players[0].pid
    player2_pid = game.players[1].pid
    game.start(player1_id)
    game.players[0].cards = []  # Ensure there is no playable card
    game.discard_pile.append(NumberCard(0, Color.RED, 0))
    game.draw_pile.append(NumberCard(0, Color.YELLOW, 1))
    game.players[0].events = []
    game.players[1].events = []
    response = game.draw_card(player1_id)
    assert response["error"] is None
    event = response["events"][2]["event"]
    assert event["name"] == "player_activated"
    assert event["player_pid"] == player2_pid
    event = game.players[1].events[1]["event"]
    assert event["name"] == "player_activated"
    assert event["player_pid"] == player2_pid


def test_draw_card_fails_if_game_abandoned(game: Game) -> None:
    game.status == GameStatus.ABANDONED
    player_id = game.players[0].id
    response = game.draw_card(player_id)
    assert response["error"] == "invalid_status"


def test_draw_card_fails_if_game_created(game: Game) -> None:
    game.status == GameStatus.CREATED
    player_id = game.players[0].id
    response = game.draw_card(player_id)
    assert response["error"] == "invalid_status"


def test_draw_card_fails_if_game_finished(game: Game) -> None:
    game.status == GameStatus.FINISHED
    player_id = game.players[0].id
    response = game.draw_card(player_id)
    assert response["error"] == "invalid_status"


def test_draw_card_fails_if_has_playable_card(game: Game) -> None:
    game.join()
    player1_id = game.players[0].id
    game.start(player1_id)
    game.discard_pile.append(NumberCard(0, Color.RED, 0))
    game.players[0].cards.append(NumberCard(0, Color.RED, 0))
    response = game.draw_card(player1_id)
    assert response["error"] == "has_playable_card"


def test_draw_card_fails_if_out_of_turn(game: Game) -> None:
    game.join()
    player1_id = game.players[0].id
    player2_id = game.players[1].id
    game.start(player1_id)
    response = game.draw_card(player2_id)
    assert response["error"] == "out_of_turn"


def test_draw_card_fails_if_player_not_found(game: Game) -> None:
    response = game.draw_card("bad_player_id")
    assert response["error"] == "player_not_found"


def test_draw_card_queues_drew_card_event(game: Game) -> None:
    game.join()
    player1_id = game.players[0].id
    game.start(player1_id)
    game.players[0].cards = []  # Ensure there is no playable card
    game.players[0].events = []
    response = game.draw_card(player1_id)
    assert response["error"] is None
    assert response["events"][0]["event"]["name"] == "drew_card"
    assert response["events"][0]["event"]["card"] == game.players[0].cards[0]


def test_draw_card_queues_player_drew_card_event(game: Game) -> None:
    game.join()
    player1_id = game.players[0].id
    player1_pid = game.players[0].pid
    game.start(player1_id)
    game.players[0].cards = []  # Ensure there is no playable card
    game.players[0].events = []
    game.players[1].events = []
    response = game.draw_card(player1_id)
    assert response["error"] is None
    event = response["events"][1]["event"]
    assert event["name"] == "player_drew_card"
    assert event["player_pid"] == player1_pid
    event = game.players[1].events[0]["event"]
    assert event["name"] == "player_drew_card"
    assert event["player_pid"] == player1_pid
