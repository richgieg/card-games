import { motion } from "framer-motion";
import { Card } from "../../../client/cards";
import { CardView } from "./CardView";

type Props = {
  card: Card;
  onClick: () => void;
};

export function CardButton({ card, onClick }: Props) {
  return (
    <motion.button
      onClick={onClick}
      whileHover={{
        scale: 1.05,
        rotate: "-2deg",
        transition: { duration: 0.15 },
      }}
      whileTap={{
        scale: 0.95,
        rotate: "-5deg",
        transition: { duration: 0.15 },
      }}
      initial={{ x: "-100vw" }}
      animate={{ x: 0, transition: { duration: 0.75, ease: "backOut" } }}
      exit={{
        x: "-100vw",
        transition: { duration: 0.5, ease: "backIn" },
      }}
    >
      <CardView card={card} />
    </motion.button>
  );
}
