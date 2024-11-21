import random
from typing import Sequence
from uuid import uuid4

from .avatars import get_random_avatar
from .cards import Action, ActionCard, Card, cards, Color, DiscardedCard, DiscardedWildCard, NumberCard, WildCard
from .constants import ACTION_CARD_POINTS, CARDS_PER_PLAYER, GameStatus, MAX_PLAYERS, MIN_PLAYERS, POINTS_TO_WIN, WILD_CARD_POINTS
from .errors import (
    CardIsWildError, CardNotFoundError, CardNotPlayableError, CardNotWildError,
    HasPlayableCardError, InvalidStatusError, MaxPlayersReachedError,
    MinPlayersNotReachedError, NotAdminError, OutOfTurnError, PlayerNotFoundError
)
from .events import (
    DrewCardEvent, DrewFourCardsEvent, DrewTwoCardsEvent, Event, GameAbandonedEvent, GameFinishedEvent,
    GameReversedEvent, GameStartedEvent, InitialDiscardEvent, PlayerActivatedEvent,
    PlayerDrewCardEvent, PlayerDrewFourCardsEvent, PlayerDrewTwoCardsEvent,
    PlayerJoinedEvent, PlayerLeftEvent, PlayerPlayedCardEvent, PlayerReceivedCardsFromDealerEvent,
    PlayerSkippedEvent, ReceivedCardsFromDealerEvent, RoundStartedEvent, RoundWonEvent
)
from .player import Player
from .responses import (
    DrawCardResponse, GetEventsResponse, GetStateResponse, JoinResponse,
    LeaveResponse, PlayCardResponse, PlayWildCardResponse, StartResponse
)


class Game:

    id: str
    status: GameStatus
    players: list[Player]
    draw_pile: list[Card]
    discard_pile: list[DiscardedCard]
    active_player_index: int
    reversed: bool

    def __init__(self) -> None:
        self.id = str(uuid4()).replace("-", "")
        self.status = GameStatus.CREATED
        self.players = [Player(get_random_avatar())]
        self.draw_pile = cards.copy()
        self.discard_pile = []
        self.active_player_index = 0
        self.reversed = False

    def join(self) -> JoinResponse | InvalidStatusError | MaxPlayersReachedError:
        if self.status != GameStatus.CREATED:
            return InvalidStatusError(error="invalid_status")
        if len(self.players) == MAX_PLAYERS:
            return MaxPlayersReachedError(error="max_players_reached")
        used_avatars = [p.avatar for p in self.players]
        avatar = get_random_avatar(used_avatars)
        player = Player(avatar)
        self.players.append(player)
        self._queue_event_for_all_players(
            PlayerJoinedEvent(name="player_joined",
                              player_pid=player.pid, avatar=player.avatar)
        )
        return JoinResponse(error=None, player_id=player.id)

    def leave(self, player_id: str) -> LeaveResponse | InvalidStatusError | PlayerNotFoundError:
        player = self._get_player(player_id)
        if player is None:
            return PlayerNotFoundError(error="player_not_found")
        if self.status in [GameStatus.ABANDONED, GameStatus.FINISHED]:
            return InvalidStatusError(error="invalid_status")
        self.players.remove(player)
        self._queue_event_for_all_players(PlayerLeftEvent(
            name="player_left", player_pid=player.pid))
        if self.status == GameStatus.CREATED:
            if len(self.players) == 0:
                self.status = GameStatus.ABANDONED
        elif self.status == GameStatus.STARTED:
            # TODO: Remove player, hand, and stats, and return their cards.
            # Also set active_player_index to 0 if out of bounds.
            if len(self.players) < MIN_PLAYERS:
                self.status = GameStatus.ABANDONED
                self._queue_event_for_all_players(
                    GameAbandonedEvent(name="game_abandoned"))
            else:
                pass
        return LeaveResponse(error=None)

    def start(self, player_id: str) -> (
        StartResponse
        | InvalidStatusError
        | MinPlayersNotReachedError
        | NotAdminError
        | PlayerNotFoundError
    ):
        player = self._get_player(player_id)

        if player is None:
            return PlayerNotFoundError(error="player_not_found")
        if self.status != GameStatus.CREATED:
            return InvalidStatusError(error="invalid_status")
        if not self._player_is_admin(player):
            return NotAdminError(error="not_admin")
        if len(self.players) < MIN_PLAYERS:
            return MinPlayersNotReachedError(error="min_players_not_reached")

        self._deal_cards_to_players()
        for p in self.players:
            p.queue_event(ReceivedCardsFromDealerEvent(
                name="received_cards_from_dealer", cards=p.cards))
        for p in self.players:
            self._queue_event_for_all_players(PlayerReceivedCardsFromDealerEvent(
                name="player_received_cards_from_dealer", player_pid=p.pid,
                count=len(p.cards)))

        self._discard_top_card()
        self._queue_event_for_all_players(InitialDiscardEvent(
            name="initial_discard", card=self.discard_pile[-1]))

        self.status = GameStatus.STARTED
        self._queue_event_for_all_players(
            GameStartedEvent(name="game_started"))

        events = player.get_events()
        player.clear_events()
        return StartResponse(error=None, events=events)

    def draw_card(self, player_id: str) -> (
        DrawCardResponse
        | HasPlayableCardError
        | InvalidStatusError
        | OutOfTurnError
        | PlayerNotFoundError
    ):
        player = self._get_player(player_id)

        if player is None:
            return PlayerNotFoundError(error="player_not_found")
        if self.status != GameStatus.STARTED:
            return InvalidStatusError(error="invalid_status")
        if self.players.index(player) != self.active_player_index:
            return OutOfTurnError(error="out_of_turn")
        if player.has_playable_card(self.discard_pile):
            return HasPlayableCardError(error="has_playable_card")

        card = self._do_draw_card()
        player.cards.append(card)

        player.queue_event(DrewCardEvent(name="drew_card", card=card))
        self._queue_event_for_all_players(PlayerDrewCardEvent(
            name="player_drew_card", player_pid=player.pid))

        if not player.has_playable_card(self.discard_pile):
            self._activate_next_player()
            active_player_pid = self.players[self.active_player_index].pid
            self._queue_event_for_all_players(PlayerActivatedEvent(
                name="player_activated", player_pid=active_player_pid))

        events = player.get_events()
        player.clear_events()
        return DrawCardResponse(error=None, events=events)

    def play_card(self, player_id: str, card_id: int) -> (
        PlayCardResponse
        | CardIsWildError
        | CardNotFoundError
        | CardNotPlayableError
        | InvalidStatusError
        | OutOfTurnError
        | PlayerNotFoundError
    ):
        player = self._get_player(player_id)

        if player is None:
            return PlayerNotFoundError(error="player_not_found")
        if self.status != GameStatus.STARTED:
            return InvalidStatusError(error="invalid_status")
        if self.players.index(player) != self.active_player_index:
            return OutOfTurnError(error="out_of_turn")

        card = player.get_card(card_id)

        if card is None:
            return CardNotFoundError(error="card_not_found")
        if isinstance(card, WildCard):
            return CardIsWildError(error="card_is_wild")
        if not player.can_play_card(card, self.discard_pile):
            return CardNotPlayableError(error="card_not_playable")

        self.discard_pile.append(card)
        player.remove_card(card)

        self._queue_event_for_all_players(PlayerPlayedCardEvent(
            name="player_played_card", player_pid=player.pid, card=card))

        if isinstance(card, ActionCard):
            match card.action:
                case Action.DRAW_TWO:
                    self._on_draw_two_card_played()
                case Action.REVERSE:
                    self._on_reverse_card_played()
                case Action.SKIP:
                    self._on_skip_card_played()
        else:
            self._on_number_card_played()

        if len(player.cards) == 0:
            self.active_player_index = self.players.index(player)
            points = self._calculate_points()
            player.points += points
            player.rounds_won += 1
            if player.points >= POINTS_TO_WIN:
                self._on_game_won(player, points)
            else:
                self._on_round_won(player, points)
        else:
            active_player_pid = self.players[self.active_player_index].pid
            self._queue_event_for_all_players(PlayerActivatedEvent(
                name="player_activated", player_pid=active_player_pid))

        events = player.get_events()
        player.clear_events()
        return PlayCardResponse(error=None, events=events)

    def play_wild_card(self, player_id: str, card_id: int, color: Color) -> (
        PlayWildCardResponse
        | CardNotFoundError
        | CardNotPlayableError
        | CardNotWildError
        | InvalidStatusError
        | OutOfTurnError
        | PlayerNotFoundError
    ):
        player = self._get_player(player_id)

        if player is None:
            return PlayerNotFoundError(error="player_not_found")
        if self.status != GameStatus.STARTED:
            return InvalidStatusError(error="invalid_status")
        if self.players.index(player) != self.active_player_index:
            return OutOfTurnError(error="out_of_turn")

        card = player.get_card(card_id)

        if card is None:
            return CardNotFoundError(error="card_not_found")
        if not isinstance(card, WildCard):
            return CardNotWildError(error="card_not_wild")
        if not player.can_play_card(card, self.discard_pile):
            return CardNotPlayableError(error="card_not_playable")

        discarded_wild_card = DiscardedWildCard(color, card)
        self.discard_pile.append(discarded_wild_card)
        player.remove_card(card)

        self._queue_event_for_all_players(PlayerPlayedCardEvent(
            name="player_played_card", player_pid=player.pid, card=discarded_wild_card))

        if card.is_draw_four:
            self._on_wild_draw_four_card_played()
        else:
            self._on_wild_card_played()

        if len(player.cards) == 0:
            self.active_player_index = self.players.index(player)
            points = self._calculate_points()
            player.points += points
            player.rounds_won += 1
            if player.points >= POINTS_TO_WIN:
                self._on_game_won(player, points)
            else:
                self._on_round_won(player, points)
        else:
            active_player_pid = self.players[self.active_player_index].pid
            self._queue_event_for_all_players(PlayerActivatedEvent(
                name="player_activated", player_pid=active_player_pid))

        events = player.get_events()
        player.clear_events()
        return PlayWildCardResponse(error=None, events=events)

    def get_state(self, player_id: str) -> GetStateResponse | PlayerNotFoundError:
        player = self._get_player(player_id)
        if player is None:
            return PlayerNotFoundError(error="player_not_found")
        player.clear_events()
        return GetStateResponse(
            error=None,
            status=self.status,
            players=[
                {
                    "pid": p.pid,
                    "avatar": p.avatar,
                    "cards": len(p.cards),
                    "rounds_won": p.rounds_won,
                    "points": p.points
                } for p in self.players
            ],
            player_pid=player.pid,
            active_player_pid=self.players[self.active_player_index].pid,
            admin_player_pid=self.players[0].pid,
            next_event_id=player.next_event_id,
            cards=player.cards,
            reversed=self.reversed,
            last_discard=self.discard_pile[-1] if len(
                self.discard_pile) > 0 else None
        )

    def get_events(self, player_id: str) -> GetEventsResponse | PlayerNotFoundError:
        player = self._get_player(player_id)
        if player is None:
            return PlayerNotFoundError(error="player_not_found")
        events = player.get_events()
        player.clear_events()
        return GetEventsResponse(error=None, events=events)

    def _activate_next_player(self) -> None:
        increment = -1 if self.reversed else 1
        self.active_player_index = (
            self.active_player_index + increment) % len(self.players)

    def _add_discarded_cards_to_draw_pile(self, discarded_cards: Sequence[DiscardedCard]) -> None:
        for discarded_card in discarded_cards:
            if isinstance(discarded_card, DiscardedWildCard):
                self.draw_pile.append(discarded_card.card)
            else:
                self.draw_pile.append(discarded_card)

    def _calculate_points(self) -> int:
        points = 0
        for player in self.players:
            for card in player.cards:
                if isinstance(card, NumberCard):
                    points += card.number
                elif isinstance(card, ActionCard):
                    points += ACTION_CARD_POINTS
                else:
                    points += WILD_CARD_POINTS
        return points

    def _deal_cards_to_players(self) -> None:
        random.shuffle(self.draw_pile)
        for _ in range(0, CARDS_PER_PLAYER):
            for player in self.players:
                card = self.draw_pile.pop()
                player.add_card(card)

    def _discard_top_card(self) -> None:
        # Move top card to bottom until top is a number card. This is temporary.
        # Will be removed once logic is in place to handle the first card being
        # a non-number card.
        top_card = self.draw_pile[-1]
        while not isinstance(top_card, NumberCard):
            self.draw_pile.insert(0, self.draw_pile.pop())
            top_card = self.draw_pile[-1]
        self.draw_pile.pop()
        self.discard_pile.append(top_card)

    def _do_draw_card(self) -> Card:
        card = self.draw_pile.pop()
        if len(self.draw_pile) == 0:
            self._add_discarded_cards_to_draw_pile(self.discard_pile[:-1])
            self.discard_pile = self.discard_pile[-1:]
            random.shuffle(self.draw_pile)
        return card

    def _get_player(self, player_id: str) -> Player | None:
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def _on_draw_two_card_played(self) -> None:
        source_player = self.players[self.active_player_index]
        self._activate_next_player()
        target_player = self.players[self.active_player_index]
        cards = (self._do_draw_card(), self._do_draw_card())
        target_player.cards.extend(cards)
        self._activate_next_player()
        target_player.queue_event(DrewTwoCardsEvent(
            name="drew_two_cards", cards=cards))
        self._queue_event_for_all_players(PlayerDrewTwoCardsEvent(
            name="player_drew_two_cards", player_pid=target_player.pid,
            source_player_pid=source_player.pid))

    def _on_game_won(self, player: Player, points: int) -> None:
        self._queue_event_for_all_players(RoundWonEvent(
            name="round_won", player_pid=player.pid, points=points))
        self.status = GameStatus.FINISHED
        self._queue_event_for_all_players(
            GameFinishedEvent(name="game_finished"))

    def _on_number_card_played(self) -> None:
        self._activate_next_player()

    def _on_reverse_card_played(self) -> None:
        if len(self.players) > 2:
            self.reversed = not self.reversed
            source_player_pid = self.players[self.active_player_index].pid
            self._activate_next_player()
            self._queue_event_for_all_players(GameReversedEvent(
                name="game_reversed", source_player_pid=source_player_pid))
        else:
            source_player_pid = self.players[self.active_player_index].pid
            self._activate_next_player()
            player_pid = self.players[self.active_player_index].pid
            self._activate_next_player()
            self._queue_event_for_all_players(PlayerSkippedEvent(
                name="player_skipped", player_pid=player_pid, source_player_pid=source_player_pid))

    def _on_round_won(self, player: Player, points: int) -> None:
        self._queue_event_for_all_players(RoundWonEvent(
            name="round_won", player_pid=player.pid, points=points))

        for p in self.players:
            self.draw_pile.extend(p.cards)
            p.cards.clear()
        self._add_discarded_cards_to_draw_pile(self.discard_pile)
        self.discard_pile.clear()

        self._deal_cards_to_players()
        for p in self.players:
            p.queue_event(ReceivedCardsFromDealerEvent(
                name="received_cards_from_dealer", cards=p.cards))
        for p in self.players:
            self._queue_event_for_all_players(PlayerReceivedCardsFromDealerEvent(
                name="player_received_cards_from_dealer", player_pid=p.pid,
                count=len(p.cards)))

        self._discard_top_card()
        self._queue_event_for_all_players(InitialDiscardEvent(
            name="initial_discard", card=self.discard_pile[-1]))

        self.reversed = False
        self._queue_event_for_all_players(
            RoundStartedEvent(name="round_started", reversed=self.reversed))

    def _on_skip_card_played(self) -> None:
        source_player_pid = self.players[self.active_player_index].pid
        self._activate_next_player()
        player_pid = self.players[self.active_player_index].pid
        self._activate_next_player()
        self._queue_event_for_all_players(PlayerSkippedEvent(
            name="player_skipped", player_pid=player_pid, source_player_pid=source_player_pid))

    def _on_wild_card_played(self) -> None:
        self._activate_next_player()

    def _on_wild_draw_four_card_played(self) -> None:
        source_player = self.players[self.active_player_index]
        self._activate_next_player()
        target_player = self.players[self.active_player_index]
        cards = (self._do_draw_card(), self._do_draw_card(),
                 self._do_draw_card(), self._do_draw_card())
        target_player.cards.extend(cards)
        self._activate_next_player()
        target_player.queue_event(DrewFourCardsEvent(
            name="drew_four_cards", cards=cards))
        self._queue_event_for_all_players(PlayerDrewFourCardsEvent(
            name="player_drew_four_cards", player_pid=target_player.pid,
            source_player_pid=source_player.pid))

    def _player_is_admin(self, player: Player) -> bool:
        return player.id == self.players[0].id

    def _queue_event_for_all_players(self, event: Event) -> None:
        for player in self.players:
            player.queue_event(event)
