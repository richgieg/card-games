import { Card, DiscardedCard } from "./cards";
import { EventWithId } from "./events";

export type CreateResponse = {
  error: null;
  game_id: string;
  player_id: string;
};

export type DrawCardResponse = {
  error: null;
  events: EventWithId[];
};

export type GetEventsResponse = {
  error: null;
  events: EventWithId[];
};

export type GetStateResponse = {
  error: null;
  status: "abandoned" | "created" | "finished" | "started";
  players: {
    pid: string;
    avatar: {
      emoji: string;
      name: string;
    };
    cards: number;
    rounds_won: number;
    points: number;
  }[];
  player_pid: string;
  active_player_pid: string;
  admin_player_pid: string;
  next_event_id: number;
  cards: Card[];
  reversed: boolean;
  last_discard: DiscardedCard | null;
};

export type JoinResponse = {
  error: null;
  player_id: string;
};

export type LeaveResponse = {
  error: null;
};

export type ListResponse = {
  error: null;
  games: {
    id: string;
    status: "abandoned" | "created" | "finished" | "started";
    players: number;
  }[];
};

export type PlayCardResponse = {
  error: null;
  events: EventWithId[];
};

export type PlayWildCardResponse = {
  error: null;
  events: EventWithId[];
};

export type StartResponse = {
  error: null;
  events: EventWithId[];
};
