from src.uno.constants import CARDS_PER_PLAYER, GameStatus
from src.uno.game import Game


def test_start(game: Game) -> None:
    game.join()
    admin_player_id = game.players[0].id
    response = game.start(admin_player_id)
    assert response["error"] is None
    assert game.status == GameStatus.STARTED
    assert len(game.players[0].cards) == CARDS_PER_PLAYER
    assert len(game.players[1].cards) == CARDS_PER_PLAYER
    assert len(game.discard_pile) == 1


def test_start_clears_player_events(game: Game) -> None:
    game.join()
    admin_player_id = game.players[0].id
    game.start(admin_player_id)
    assert len(game.players[0].events) == 0


def test_start_fails_if_game_abandoned(game: Game) -> None:
    game.join()
    admin_player_id = game.players[0].id
    game.status = GameStatus.ABANDONED
    response = game.start(admin_player_id)
    assert response["error"] == "invalid_status"


def test_start_fails_if_game_finished(game: Game) -> None:
    game.join()
    admin_player_id = game.players[0].id
    game.status = GameStatus.FINISHED
    response = game.start(admin_player_id)
    assert response["error"] == "invalid_status"


def test_start_fails_if_game_started(game: Game) -> None:
    game.join()
    admin_player_id = game.players[0].id
    game.status = GameStatus.STARTED
    response = game.start(admin_player_id)
    assert response["error"] == "invalid_status"


def test_start_fails_if_min_players_not_reached(game: Game) -> None:
    admin_player_id = game.players[0].id
    response = game.start(admin_player_id)
    assert response["error"] == "min_players_not_reached"


def test_start_fails_if_player_not_admin(game: Game) -> None:
    game.join()
    player2_id = game.players[1].id
    response = game.start(player2_id)
    assert response["error"] == "not_admin"


def test_start_fails_if_player_not_found(game: Game) -> None:
    game.join()
    response = game.start("bad_player_id")
    assert response["error"] == "player_not_found"


def test_start_queues_events(game: Game) -> None:
    game.join()
    admin_player_id = game.players[0].id
    for player in game.players:
        player.events.clear()
    response = game.start(admin_player_id)
    assert response["error"] is None
    # Check player 1 events.
    event1 = response["events"][0]["event"]
    assert event1["name"] == "received_cards_from_dealer"
    assert event1["cards"] == game.players[0].cards
    event2 = response["events"][1]["event"]
    assert event2["name"] == "player_received_cards_from_dealer"
    assert event2["count"] == CARDS_PER_PLAYER
    event3 = response["events"][2]["event"]
    assert event3["name"] == "player_received_cards_from_dealer"
    assert event3["count"] == CARDS_PER_PLAYER
    event4 = response["events"][3]["event"]
    assert event4["name"] == "initial_discard"
    assert event4["card"] == game.discard_pile[-1]
    event5 = response["events"][4]["event"]
    assert event5["name"] == "game_started"
    # Check player 2 events.
    event1 = game.players[1].events[0]["event"]
    assert event1["name"] == "received_cards_from_dealer"
    assert event1["cards"] == game.players[1].cards
    event2 = game.players[1].events[1]["event"]
    assert event2["name"] == "player_received_cards_from_dealer"
    assert event2["count"] == CARDS_PER_PLAYER
    event3 = game.players[1].events[2]["event"]
    assert event3["name"] == "player_received_cards_from_dealer"
    assert event3["count"] == CARDS_PER_PLAYER
    event4 = game.players[1].events[3]["event"]
    assert event4["name"] == "initial_discard"
    assert event4["card"] == game.discard_pile[-1]
    event5 = game.players[1].events[4]["event"]
    assert event5["name"] == "game_started"
