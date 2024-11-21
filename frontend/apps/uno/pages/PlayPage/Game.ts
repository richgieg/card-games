import Router from "next/router";
import { configure, makeAutoObservable } from "mobx";
import { client } from "../../client";
import { Card, Color } from "../../client/cards";
import { EventWithId } from "../../client/events";
import { GetStateResponse } from "../../client/responses";

configure({ enforceActions: "never" });

export class Game {
  private readonly gameId: string;
  private readonly playerId: string;
  private readonly intervalId: number;
  public state: GetStateResponse;

  constructor(
    gameId: string,
    playerId: string,
    initialState: GetStateResponse
  ) {
    this.gameId = gameId;
    this.playerId = playerId;
    this.state = initialState;
    this.intervalId = window.setInterval(
      () => this.getAndProcessEvents(),
      1000
    );
    makeAutoObservable(this);
  }

  async leave() {
    if (this.state.status === "abandoned" || this.state.status === "finished") {
      Router.push("/uno");
      return;
    }
    const response = await client.leave(this.gameId, this.playerId);
    if (response.error) {
      alert(response.error);
    } else {
      window.clearInterval(this.intervalId);
      Router.push("/uno");
    }
  }

  async start() {
    const response = await client.start(this.gameId, this.playerId);
    if (response.error) {
      alert(response.error);
    } else {
      this.processEvents(response.events);
    }
  }

  async playCard(card: Card) {
    let response:
      | Awaited<ReturnType<(typeof client)["playCard"]>>
      | Awaited<ReturnType<(typeof client)["playWildCard"]>>;
    if (card.kind === "wild") {
      const color = prompt("blue, green, red, yellow") as Color;
      response = await client.playWildCard(
        this.gameId,
        this.playerId,
        card.id,
        color
      );
    } else {
      response = await client.playCard(this.gameId, this.playerId, card.id);
    }
    if (response.error) {
      alert(response.error);
    } else {
      this.processEvents(response.events);
    }
  }

  async drawCard() {
    const response = await client.drawCard(this.gameId, this.playerId);
    if (response.error) {
      alert(response.error);
    } else {
      this.processEvents(response.events);
    }
  }

  destroy() {
    window.clearInterval(this.intervalId);
  }

  private async getAndProcessEvents() {
    const response = await client.getEvents(this.gameId, this.playerId);
    if (response.error) {
      alert(response.error);
    } else {
      this.processEvents(response.events);
    }
  }

  private processEvents(events: EventWithId[]) {
    for (const event of events) {
      this.processEvent(event);
    }
  }

  private processEvent(event: EventWithId) {
    const e = event.event;
    switch (e.name) {
      case "admin_changed": {
        this.state.admin_player_pid = e.player_pid;
        break;
      }
      case "drew_card": {
        this.state.cards.push(e.card);
        break;
      }
      case "drew_four_cards": {
        window.setTimeout(() => {
          this.state.cards.push(...e.cards);
        }, 1750);
        break;
      }
      case "drew_two_cards": {
        window.setTimeout(() => {
          this.state.cards.push(...e.cards);
        }, 1750);
        break;
      }
      case "game_abandoned": {
        this.state.status = "abandoned";
        break;
      }
      case "game_finished": {
        this.state.status = "finished";
        break;
      }
      case "game_reversed": {
        this.state.reversed = !this.state.reversed;
        break;
      }
      case "game_started": {
        this.state.status = "started";
        break;
      }
      case "initial_discard": {
        window.setTimeout(() => {
          this.state.last_discard = e.card;
        }, 4500);
        break;
      }
      case "player_activated": {
        this.state.active_player_pid = e.player_pid;
        break;
      }
      case "player_drew_card": {
        const player = this.state.players.find((p) => p.pid === e.player_pid);
        if (player) {
          player.cards++;
        }
        break;
      }
      case "player_drew_four_cards": {
        const player = this.state.players.find((p) => p.pid === e.player_pid);
        if (player) {
          player.cards += 4;
        }
        break;
      }
      case "player_drew_two_cards": {
        const player = this.state.players.find((p) => p.pid === e.player_pid);
        if (player) {
          player.cards += 2;
        }
        break;
      }
      case "player_joined": {
        this.state.players.push({
          pid: e.player_pid,
          avatar: e.avatar,
          cards: 0,
          rounds_won: 0,
          points: 0,
        });
        break;
      }
      case "player_left": {
        this.state.players = this.state.players.filter(
          (p) => p.pid !== e.player_pid
        );
        break;
      }
      case "player_played_card": {
        const player = this.state.players.find((p) => p.pid === e.player_pid);
        if (player) {
          player.cards--;
        }
        if (this.state.player_pid === e.player_pid) {
          const cardId =
            e.card.kind === "discarded_wild" ? e.card.card.id : e.card.id;
          this.state.cards = this.state.cards.filter((c) => c.id !== cardId);
        }
        this.state.last_discard = e.card;
        break;
      }
      case "player_received_cards_from_dealer": {
        const player = this.state.players.find((p) => p.pid === e.player_pid);
        if (player) {
          player.cards = e.count;
        }
        break;
      }
      case "player_skipped": {
        break;
      }
      case "received_cards_from_dealer": {
        window.setTimeout(() => {
          this.state.cards.push(...e.cards);
        }, 4000);
        break;
      }
      case "round_started": {
        window.setTimeout(() => {
          this.state.last_discard = null;
          this.state.reversed = e.reversed;
        }, 2500);
        break;
      }
      case "round_won": {
        window.setTimeout(() => {
          const player = this.state.players.find((p) => p.pid === e.player_pid);
          if (player) {
            player.points += e.points;
            player.rounds_won++;
          }
          this.state.cards = [];
        }, 2000);
        break;
      }
    }
  }
}
