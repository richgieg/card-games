from typing import TypedDict

from .avatars import Avatar
from .cards import Card, DiscardedCard
from .constants import GameStatus
from .events import EventWithId


class CreateResponse(TypedDict):
    error: None
    game_id: str
    player_id: str


class DrawCardResponse(TypedDict):
    error: None
    events: list[EventWithId]


class GetEventsResponse(TypedDict):
    error: None
    events: list[EventWithId]


class Player(TypedDict):
    pid: str
    avatar: Avatar
    cards: int
    rounds_won: int
    points: int


class GetStateResponse(TypedDict):
    error: None
    status: GameStatus
    players: list[Player]
    player_pid: str
    active_player_pid: str
    admin_player_pid: str
    next_event_id: int
    cards: list[Card]
    reversed: bool
    last_discard: DiscardedCard | None


class JoinResponse(TypedDict):
    error: None
    player_id: str


class LeaveResponse(TypedDict):
    error: None


class Game(TypedDict):
    id: str
    status: GameStatus
    players: int


class ListResponse(TypedDict):
    error: None
    games: list[Game]


class PlayCardResponse(TypedDict):
    error: None
    events: list[EventWithId]


class PlayWildCardResponse(TypedDict):
    error: None
    events: list[EventWithId]


class StartResponse(TypedDict):
    error: None
    events: list[EventWithId]
