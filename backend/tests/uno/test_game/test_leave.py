from src.uno.game import Game


def test_leave(game: Game) -> None:
    join_response = game.join()
    assert join_response["error"] is None
    player_id = join_response["player_id"]
    leave_response = game.leave(player_id)
    assert leave_response["error"] is None


def test_leave_fails_if_player_not_found(game: Game) -> None:
    response = game.leave("bad_player_id")
    assert response["error"] == "player_not_found"


def test_leave_queues_player_activated_event(game: Game) -> None:
    pass


def test_leave_queues_player_left_event(game: Game) -> None:
    join_response = game.join()
    assert join_response["error"] is None
    player_id = join_response["player_id"]
    player_pid = game.players[1].pid
    game.players[0].events = []
    game.leave(player_id)
    event = game.players[0].events[0]["event"]
    assert event["name"] == "player_left"
    assert event["player_pid"] == player_pid


def test_leave_removes_player(game: Game) -> None:
    join_response = game.join()
    assert join_response["error"] is None
    player_id = join_response["player_id"]
    game.leave(player_id)
    assert len(game.players) == 1
    assert game.players[0].id != player_id


def test_leave_returns_player_cards_to_discard_pile(game: Game) -> None:
    pass


def test_leave_updates_active_player_index(game: Game) -> None:
    pass
