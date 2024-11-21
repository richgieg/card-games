from typing import Sequence
from uuid import uuid4

from .avatars import Avatar
from .cards import ActionCard, Card, Color, DiscardedCard, NumberCard, WildCard
from .events import Event, EventWithId


class Player:

    id: str
    pid: str
    avatar: Avatar
    cards: list[Card]
    events: list[EventWithId]
    next_event_id: int
    rounds_won: int
    points: int

    def __init__(self, avatar: Avatar) -> None:
        self.id = str(uuid4()).replace("-", "")
        self.pid = str(uuid4()).replace("-", "")
        self.avatar = avatar
        self.cards = []
        self.events = []
        self.next_event_id = 0
        self.rounds_won = 0
        self.points = 0

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def remove_card(self, card: Card) -> None:
        self.cards.remove(card)

    def get_card(self, card_id: int) -> Card | None:
        for c in self.cards:
            if c.id == card_id:
                return c
        return None

    def has_playable_card(self, discard_pile: Sequence[DiscardedCard]) -> bool:
        for card in self.cards:
            if self.can_play_card(card, discard_pile):
                return True
        return False

    def can_play_card(self, card: Card, discard_pile: Sequence[DiscardedCard]) -> bool:
        if not card in self.cards:
            return False
        last_discard = discard_pile[-1]
        if isinstance(card, WildCard):
            if card.is_draw_four and self._has_card_of_color(last_discard.color):
                return False
            return True
        if card.color == last_discard.color:
            return True
        if isinstance(card, ActionCard) and isinstance(last_discard, ActionCard):
            return card.action == last_discard.action
        if isinstance(card, NumberCard) and isinstance(last_discard, NumberCard):
            return card.number == last_discard.number
        return False

    def get_events(self) -> list[EventWithId]:
        return self.events.copy()

    def clear_events(self) -> None:
        self.events.clear()

    def queue_event(self, event: Event) -> None:
        self.events.append({"id": self.next_event_id, "event": event})
        self.next_event_id += 1

    def _has_card_of_color(self, color: Color) -> bool:
        for card in self.cards:
            if not isinstance(card, WildCard) and card.color == color:
                return True
        return False
