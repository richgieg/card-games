from typing import Literal, TypedDict

from .avatars import Avatar
from .cards import Card, DiscardedCard


class AdminChangedEvent(TypedDict):
    name: Literal["admin_changed"]
    player_pid: str


class DrewCardEvent(TypedDict):
    name: Literal["drew_card"]
    card: Card


class DrewFourCardsEvent(TypedDict):
    name: Literal["drew_four_cards"]
    cards: tuple[Card, Card, Card, Card]


class DrewTwoCardsEvent(TypedDict):
    name: Literal["drew_two_cards"]
    cards: tuple[Card, Card]


class GameAbandonedEvent(TypedDict):
    name: Literal["game_abandoned"]


class GameFinishedEvent(TypedDict):
    name: Literal["game_finished"]


class GameReversedEvent(TypedDict):
    name: Literal["game_reversed"]
    source_player_pid: str


class GameStartedEvent(TypedDict):
    name: Literal["game_started"]


class InitialDiscardEvent(TypedDict):
    name: Literal["initial_discard"]
    card: DiscardedCard


class PlayerActivatedEvent(TypedDict):
    name: Literal["player_activated"]
    player_pid: str


class PlayerDrewCardEvent(TypedDict):
    name: Literal["player_drew_card"]
    player_pid: str


class PlayerDrewFourCardsEvent(TypedDict):
    name: Literal["player_drew_four_cards"]
    player_pid: str
    source_player_pid: str


class PlayerDrewTwoCardsEvent(TypedDict):
    name: Literal["player_drew_two_cards"]
    player_pid: str
    source_player_pid: str


class PlayerJoinedEvent(TypedDict):
    name: Literal["player_joined"]
    player_pid: str
    avatar: Avatar


class PlayerLeftEvent(TypedDict):
    name: Literal["player_left"]
    player_pid: str


class PlayerPlayedCardEvent(TypedDict):
    name: Literal["player_played_card"]
    player_pid: str
    card: DiscardedCard


class PlayerReceivedCardsFromDealerEvent(TypedDict):
    name: Literal["player_received_cards_from_dealer"]
    player_pid: str
    count: int


class PlayerSkippedEvent(TypedDict):
    name: Literal["player_skipped"]
    player_pid: str
    source_player_pid: str


class ReceivedCardsFromDealerEvent(TypedDict):
    name: Literal["received_cards_from_dealer"]
    cards: list[Card]


class RoundStartedEvent(TypedDict):
    name: Literal["round_started"]
    reversed: bool


class RoundWonEvent(TypedDict):
    name: Literal["round_won"]
    player_pid: str
    points: int


Event = (
    AdminChangedEvent
    | DrewCardEvent
    | DrewFourCardsEvent
    | DrewTwoCardsEvent
    | GameAbandonedEvent
    | GameFinishedEvent
    | GameReversedEvent
    | GameStartedEvent
    | InitialDiscardEvent
    | PlayerActivatedEvent
    | PlayerDrewCardEvent
    | PlayerDrewFourCardsEvent
    | PlayerDrewTwoCardsEvent
    | PlayerJoinedEvent
    | PlayerLeftEvent
    | PlayerPlayedCardEvent
    | PlayerReceivedCardsFromDealerEvent
    | PlayerSkippedEvent
    | ReceivedCardsFromDealerEvent
    | RoundStartedEvent
    | RoundWonEvent
)


class EventWithId(TypedDict):
    id: int
    event: Event
