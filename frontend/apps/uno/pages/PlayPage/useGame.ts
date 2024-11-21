import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { client } from "../../client";
import { Game } from "./Game";

export function useGame() {
  const router = useRouter();
  const [gameId, setGameId] = useState<string | null>(null);
  const [playerId, setPlayerId] = useState<string | null>(null);
  const [game, setGame] = useState<Game | null>(null);

  useEffect(() => {
    if (!router.isReady) {
      return;
    }
    if (typeof router.query.game_id !== "string") {
      console.error("Missing or invalid game_id");
      return;
    }
    if (typeof router.query.player_id !== "string") {
      console.error("Missing or invalid player_id");
      return;
    }
    setGameId(router.query.game_id);
    setPlayerId(router.query.player_id);
  }, [router]);

  useEffect(() => {
    if (!gameId || !playerId) {
      return;
    }
    const getState = async () => {
      const response = await client.getState(gameId, playerId);
      if (response.error) {
        alert(response.error);
      } else {
        setGame(new Game(gameId, playerId, response));
      }
    };
    getState();
  }, [gameId, playerId]);

  useEffect(() => {
    return () => {
      if (game) {
        game.destroy();
      }
    };
  }, [game]);

  return game;
}
