export type CardIsWildError = {
  error: "card_is_wild";
};

export type CardNotFoundError = {
  error: "card_not_found";
};

export type CardNotPlayableError = {
  error: "card_not_playable";
};

export type CardNotWildError = {
  error: "card_not_wild";
};

export type GameNotFoundError = {
  error: "game_not_found";
};

export type HasPlayableCardError = {
  error: "has_playable_card";
};

export type InvalidStatusError = {
  error: "invalid_status";
};

export type MinPlayersNotReachedError = {
  error: "min_players_not_reached";
};

export type MaxGamesReachedError = {
  error: "max_games_reached";
};

export type MaxPlayersReachedError = {
  error: "max_players_reached";
};

export type NotAdminError = {
  error: "not_admin";
};

export type OutOfTurnError = {
  error: "out_of_turn";
};

export type PlayerNotFoundError = {
  error: "player_not_found";
};
