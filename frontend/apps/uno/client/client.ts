import { Color } from "./cards";
import {
  CardIsWildError,
  CardNotFoundError,
  CardNotPlayableError,
  CardNotWildError,
  GameNotFoundError,
  HasPlayableCardError,
  InvalidStatusError,
  MaxGamesReachedError,
  MaxPlayersReachedError,
  MinPlayersNotReachedError,
  NotAdminError,
  OutOfTurnError,
  PlayerNotFoundError,
} from "./errors";
import {
  CreateResponse,
  DrawCardResponse,
  GetEventsResponse,
  GetStateResponse,
  JoinResponse,
  LeaveResponse,
  ListResponse,
  PlayCardResponse,
  PlayWildCardResponse,
  StartResponse,
} from "./responses";

class Client {
  async list(): Promise<ListResponse> {
    return await this.get("/uno/list");
  }

  async create(): Promise<CreateResponse | MaxGamesReachedError> {
    return await this.post("/uno/create");
  }

  async join(
    game_id: string
  ): Promise<
    | JoinResponse
    | GameNotFoundError
    | InvalidStatusError
    | MaxPlayersReachedError
  > {
    return await this.post(`/uno/join?game_id=${game_id}`);
  }

  async leave(
    game_id: string,
    player_id: string
  ): Promise<LeaveResponse | GameNotFoundError | PlayerNotFoundError> {
    return await this.post(
      `/uno/leave?game_id=${game_id}&player_id=${player_id}`
    );
  }

  async start(
    game_id: string,
    player_id: string
  ): Promise<
    | StartResponse
    | GameNotFoundError
    | InvalidStatusError
    | MinPlayersNotReachedError
    | NotAdminError
    | PlayerNotFoundError
  > {
    return await this.post(
      `/uno/start?game_id=${game_id}&player_id=${player_id}`
    );
  }

  async drawCard(
    game_id: string,
    player_id: string
  ): Promise<
    | DrawCardResponse
    | GameNotFoundError
    | HasPlayableCardError
    | InvalidStatusError
    | OutOfTurnError
    | PlayerNotFoundError
  > {
    return await this.post(
      `/uno/draw-card?game_id=${game_id}&player_id=${player_id}`
    );
  }

  async playCard(
    game_id: string,
    player_id: string,
    card_id: number
  ): Promise<
    | PlayCardResponse
    | CardIsWildError
    | CardNotFoundError
    | CardNotPlayableError
    | GameNotFoundError
    | InvalidStatusError
    | OutOfTurnError
    | PlayerNotFoundError
  > {
    return await this.post(
      `/uno/play-card?game_id=${game_id}&player_id=${player_id}&card_id=${card_id}`
    );
  }

  async playWildCard(
    game_id: string,
    player_id: string,
    card_id: number,
    color: Color
  ): Promise<
    | PlayWildCardResponse
    | CardNotFoundError
    | CardNotPlayableError
    | CardNotWildError
    | GameNotFoundError
    | InvalidStatusError
    | OutOfTurnError
    | PlayerNotFoundError
  > {
    return await this.post(
      `/uno/play-wild-card?game_id=${game_id}&player_id=${player_id}&card_id=${card_id}&color=${color}`
    );
  }

  async getState(
    game_id: string,
    player_id: string
  ): Promise<GetStateResponse | GameNotFoundError | PlayerNotFoundError> {
    return await this.get(
      `/uno/get-state?game_id=${game_id}&player_id=${player_id}`
    );
  }

  async getEvents(
    game_id: string,
    player_id: string
  ): Promise<GetEventsResponse | GameNotFoundError | PlayerNotFoundError> {
    return await this.get(
      `/uno/get-events?game_id=${game_id}&player_id=${player_id}`
    );
  }

  private async get(url: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}${url}`
    );
    return await response.json();
  }

  private async post(url: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}${url}`,
      { method: "post" }
    );
    return await response.json();
  }
}

export const client = new Client();
