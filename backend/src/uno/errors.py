from typing import Literal, TypedDict


class CardIsWildError(TypedDict):
    error: Literal["card_is_wild"]


class CardNotFoundError(TypedDict):
    error: Literal["card_not_found"]


class CardNotPlayableError(TypedDict):
    error: Literal["card_not_playable"]


class CardNotWildError(TypedDict):
    error: Literal["card_not_wild"]


class GameNotFoundError(TypedDict):
    error: Literal["game_not_found"]


class HasPlayableCardError(TypedDict):
    error: Literal["has_playable_card"]


class InvalidStatusError(TypedDict):
    error: Literal["invalid_status"]


class MinPlayersNotReachedError(TypedDict):
    error: Literal["min_players_not_reached"]


class MaxGamesReachedError(TypedDict):
    error: Literal["max_games_reached"]


class MaxPlayersReachedError(TypedDict):
    error: Literal["max_players_reached"]


class NotAdminError(TypedDict):
    error: Literal["not_admin"]


class OutOfTurnError(TypedDict):
    error: Literal["out_of_turn"]


class PlayerNotFoundError(TypedDict):
    error: Literal["player_not_found"]
