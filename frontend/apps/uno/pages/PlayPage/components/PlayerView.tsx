import { observer } from "mobx-react-lite";
import { GetStateResponse } from "../../../client/responses";

type Props = {
  state: GetStateResponse;
  pid: string;
};

export const PlayerView = observer(({ state, pid }: Props) => {
  const player = state.players.find((p) => p.pid === pid)!;
  const { avatar, cards, rounds_won, points } = player;

  const className = {
    bg:
      state.status === "started" && player.pid === state.active_player_pid
        ? "bg-slate-200"
        : "bg-none",
  };

  return (
    <div
      className={`w-44 rounded-lg p-4 transition-colors duration-700 delay-1000 text-center ${className.bg}`}
    >
      <div className="text-center text-6xl">{avatar.emoji}</div>
      <div className="mt-4">
        C={cards} R={rounds_won} P={points}
      </div>
    </div>
  );
});
