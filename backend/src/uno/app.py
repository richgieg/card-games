import pickle
from pathlib import Path
from typing import Callable, Tuple

from fastapi import FastAPI

from .cards import Color
from .constants import MAX_GAMES
from .errors import (
    CardIsWildError, CardNotFoundError, CardNotPlayableError, CardNotWildError,
    GameNotFoundError, HasPlayableCardError, InvalidStatusError, MaxGamesReachedError,
    MaxPlayersReachedError, MinPlayersNotReachedError, NotAdminError, OutOfTurnError,
    PlayerNotFoundError
)
from .game import Game
from .responses import (
    CreateResponse, DrawCardResponse, GetEventsResponse, GetStateResponse, JoinResponse,
    LeaveResponse, ListResponse, PlayCardResponse, PlayWildCardResponse, StartResponse
)


LoadFunc = Callable[[], None]
SaveFunc = Callable[[], None]


def create_app() -> Tuple[FastAPI, LoadFunc, SaveFunc]:

    app = FastAPI(title="UNO API")

    games: dict[str, Game] = {}

    def load() -> None:
        print("loading uno.bin")
        nonlocal games
        file_path = Path("uno.bin")
        if file_path.exists():
            with file_path.open("rb") as file:
                games = pickle.load(file)

    def save() -> None:
        print("saving uno.bin")
        with open("uno.bin", "wb") as file:
            pickle.dump(games, file)

    @app.get("/list")
    async def list() -> ListResponse:
        return ListResponse(
            error=None,
            games=[
                {
                    "id": id,
                    "status": games[id].status,
                    "players": len(games[id].players)
                } for id in games
            ]
        )

    @app.post("/create")
    async def create() -> CreateResponse | MaxGamesReachedError:
        if len(games) >= MAX_GAMES:
            return MaxGamesReachedError(error="max_games_reached")
        game = Game()
        games[game.id] = game
        return CreateResponse(error=None, game_id=game.id, player_id=game.players[0].id)

    @app.post("/join")
    async def join(game_id: str) -> (
        JoinResponse
        | GameNotFoundError
        | InvalidStatusError
        | MaxPlayersReachedError
    ):
        game = games.get(game_id)
        if game is None:
            return GameNotFoundError(error="game_not_found")
        return game.join()

    @app.post("/leave")
    async def leave(game_id: str, player_id: str) -> (
        LeaveResponse
        | GameNotFoundError
        | InvalidStatusError
        | PlayerNotFoundError
    ):
        game = games.get(game_id)
        if game is None:
            return GameNotFoundError(error="game_not_found")
        return game.leave(player_id)

    @app.post("/start")
    async def start(game_id: str, player_id: str) -> (
        StartResponse
        | GameNotFoundError
        | InvalidStatusError
        | MinPlayersNotReachedError
        | NotAdminError
        | PlayerNotFoundError
    ):
        game = games.get(game_id)
        if game is None:
            return GameNotFoundError(error="game_not_found")
        return game.start(player_id)

    @app.post("/draw-card")
    async def draw_card(game_id: str, player_id: str) -> (
        DrawCardResponse
        | GameNotFoundError
        | HasPlayableCardError
        | InvalidStatusError
        | OutOfTurnError
        | PlayerNotFoundError
    ):
        game = games.get(game_id)
        if game is None:
            return GameNotFoundError(error="game_not_found")
        return game.draw_card(player_id)

    @app.post("/play-card")
    async def play_card(game_id: str, player_id: str, card_id: int) -> (
        PlayCardResponse
        | CardIsWildError
        | CardNotFoundError
        | CardNotPlayableError
        | GameNotFoundError
        | InvalidStatusError
        | OutOfTurnError
        | PlayerNotFoundError
    ):
        game = games.get(game_id)
        if game is None:
            return GameNotFoundError(error="game_not_found")
        return game.play_card(player_id, card_id)

    @app.post("/play-wild-card")
    async def play_wild_card(game_id: str, player_id: str, card_id: int, color: Color) -> (
        PlayWildCardResponse
        | CardNotFoundError
        | CardNotPlayableError
        | CardNotWildError
        | GameNotFoundError
        | InvalidStatusError
        | OutOfTurnError
        | PlayerNotFoundError
    ):
        game = games.get(game_id)
        if game is None:
            return GameNotFoundError(error="game_not_found")
        return game.play_wild_card(player_id, card_id, color)

    @app.get("/get-state")
    async def get_state(game_id: str, player_id: str) -> (
        GetStateResponse
        | GameNotFoundError
        | PlayerNotFoundError
    ):
        game = games.get(game_id)
        if game is None:
            return GameNotFoundError(error="game_not_found")
        return game.get_state(player_id)

    @app.get("/get-events")
    async def get_events(game_id: str, player_id: str) -> (
        GetEventsResponse
        | GameNotFoundError
        | PlayerNotFoundError
    ):
        game = games.get(game_id)
        if game is None:
            return GameNotFoundError(error="game_not_found")
        return game.get_events(player_id)

    return (app, load, save)
