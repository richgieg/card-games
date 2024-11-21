import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { client } from "../../client";
import { ListResponse } from "../../client/responses";

export function LandingPage() {
  const router = useRouter();
  const [games, setGames] = useState<ListResponse["games"]>([]);

  useEffect(() => {
    const list = async () => {
      const response = await client.list();
      setGames(response.games);
    };
    list();
  }, []);

  const create = async () => {
    const response = await client.create();
    if (response.error) {
      alert(response.error);
    } else {
      router.push(
        `/uno/play?game_id=${response.game_id}&player_id=${response.player_id}`
      );
    }
  };

  const join = async (gameId: string) => {
    const response = await client.join(gameId);
    if (response.error) {
      alert(response.error);
    } else {
      router.push(
        `/uno/play?game_id=${gameId}&player_id=${response.player_id}`
      );
    }
  };

  return (
    <div>
      <button onClick={create} className="underline text-blue-600">
        Create
      </button>
      <ul>
        {games.map((game) => (
          <li key={game.id}>
            {game.id} | {game.status} | {game.players} |{" "}
            {game.status === "created" && (
              <button
                onClick={() => join(game.id)}
                className="underline text-blue-600"
              >
                Join
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
