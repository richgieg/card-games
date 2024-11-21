from enum import Enum


MAX_GAMES = 50
MIN_PLAYERS = 2
MAX_PLAYERS = 10
CARDS_PER_PLAYER = 7
ACTION_CARD_POINTS = 20
WILD_CARD_POINTS = 50
POINTS_TO_WIN = 500


class GameStatus(Enum):
    ABANDONED = "abandoned"
    CREATED = "created"
    FINISHED = "finished"
    STARTED = "started"
