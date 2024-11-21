import { motion, AnimatePresence } from "framer-motion";
import { DiscardedCard } from "../../../client/cards";
import { CardView } from "./CardView";
import { useEffect, useState } from "react";

type Props = {
  lastDiscard: DiscardedCard | null;
};

export function DiscardPile({ lastDiscard }: Props) {
  const [lastTwoDiscardedCards, setLastTwoDiscardedCards] = useState<
    DiscardedCard[]
  >([]);

  useEffect(() => {
    if (!lastDiscard) {
      setLastTwoDiscardedCards([]);
      return;
    }
    setLastTwoDiscardedCards((prev) => {
      const topCard = prev[prev.length - 1];
      if (topCard && lastDiscard) {
        const topCardId =
          topCard.kind === "discarded_wild" ? topCard.card.id : topCard.id;
        const lastDiscardId =
          lastDiscard.kind === "discarded_wild"
            ? lastDiscard.card.id
            : lastDiscard.id;
        if (topCardId === lastDiscardId) {
          return prev;
        }
      }
      return [...prev.slice(prev.length - 1), lastDiscard];
    });
  }, [lastDiscard]);

  return (
    <div className="relative">
      <AnimatePresence>
        <motion.div
          key={"discard"}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          <CardView card={"discard"} />
        </motion.div>
        {lastTwoDiscardedCards.map((card) => {
          const key = card.kind === "discarded_wild" ? card.card.id : card.id;
          return (
            <motion.div
              key={key}
              initial={{ x: "100vw", y: "-100vw" }}
              animate={{
                x: 0,
                y: 0,
                transition: { delay: 0.7, duration: 0.7, ease: "backOut" },
              }}
              exit={{ opacity: 0 }}
              style={{ position: "absolute", top: 0 }}
            >
              <CardView card={card} />
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
