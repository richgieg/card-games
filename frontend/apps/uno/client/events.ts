import { Card, DiscardedCard } from "./cards";

type AdminChangedEvent = {
  name: "admin_changed";
  player_pid: string;
};

type DrewCardEvent = {
  name: "drew_card";
  card: Card;
};

type DrewFourCardsEvent = {
  name: "drew_four_cards";
  cards: [Card, Card, Card, Card];
};

type DrewTwoCardsEvent = {
  name: "drew_two_cards";
  cards: [Card, Card];
};

type GameAbandonedEvent = {
  name: "game_abandoned";
};

type GameFinishedEvent = {
  name: "game_finished";
};

type GameReversedEvent = {
  name: "game_reversed";
  source_player_pid: string;
};

type GameStartedEvent = {
  name: "game_started";
};

type InitialDiscardEvent = {
  name: "initial_discard";
  card: DiscardedCard;
};

type PlayerActivatedEvent = {
  name: "player_activated";
  player_pid: string;
};

type PlayerDrewCardEvent = {
  name: "player_drew_card";
  player_pid: string;
};

type PlayerDrewFourCardsEvent = {
  name: "player_drew_four_cards";
  player_pid: string;
  source_player_pid: string;
};

type PlayerDrewTwoCardsEvent = {
  name: "player_drew_two_cards";
  player_pid: string;
  source_player_pid: string;
};

type PlayerJoinedEvent = {
  name: "player_joined";
  player_pid: string;
  avatar: {
    emoji: string;
    name: string;
  };
};

type PlayerLeftEvent = {
  name: "player_left";
  player_pid: string;
};

type PlayerPlayedCardEvent = {
  name: "player_played_card";
  player_pid: string;
  card: DiscardedCard;
};

type PlayerReceivedCardsFromDealerEvent = {
  name: "player_received_cards_from_dealer";
  player_pid: string;
  count: number;
};

type PlayerSkippedEvent = {
  name: "player_skipped";
  player_pid: string;
  source_player_pid: string;
};

type ReceivedCardsFromDealerEvent = {
  name: "received_cards_from_dealer";
  cards: Card[];
};

type RoundStartedEvent = {
  name: "round_started";
  reversed: boolean;
};

type RoundWonEvent = {
  name: "round_won";
  player_pid: string;
  points: number;
};

type Event =
  | AdminChangedEvent
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
  | RoundWonEvent;

export type EventWithId = {
  id: number;
  event: Event;
};
