"use client";

import { motion, AnimatePresence } from "framer-motion";
import { CardButton } from "./components/CardButton";
import { DrawButton } from "./components/DrawButton";
import { DiscardPile } from "./components/DiscardPile";
import { PlayerView } from "./components/PlayerView";
import { useGame } from "./useGame";
import { observer } from "mobx-react-lite";

export const PlayPage = observer(() => {
  const game = useGame();

  if (!game) {
    return <div>Loading</div>;
  }

  return (
    <div className="overflow-x-hidden min-h-screen">
      <div className="p-6 flex justify-between flex-row-reverse">
        <motion.button
          className="bg-slate-500 text-white rounded-full px-8 py-2"
          onClick={() => game.leave()}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95, rotate: "-3deg" }}
        >
          Quit
        </motion.button>
        {game.state.status === "created" &&
          game.state.player_pid === game.state.admin_player_pid && (
            <motion.button
              className="bg-green-600 text-white rounded-full px-8 py-2"
              onClick={() => game.start()}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95, rotate: "-3deg" }}
            >
              Start
            </motion.button>
          )}
      </div>

      <div className="flex gap-2 flex-wrap justify-center px-6">
        {game.state.players.map(({ pid }) => (
          <PlayerView key={pid} state={game.state} pid={pid} />
        ))}
      </div>

      <div className="flex gap-2 justify-center mt-12">
        <DiscardPile lastDiscard={game.state.last_discard} />
        <DrawButton onClick={() => game.drawCard()} />
      </div>

      <div className="flex gap-2 flex-wrap justify-center px-6 mt-12">
        <AnimatePresence>
          {game.state.cards.map((card) => (
            <CardButton
              key={card.id}
              card={card}
              onClick={() => game.playCard(card)}
            />
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
});
