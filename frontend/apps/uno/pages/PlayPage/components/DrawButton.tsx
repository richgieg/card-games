import { motion } from "framer-motion";

const className =
  "flex justify-center items-center text-center w-28 h-36 border-black border-2 rounded-2xl text-xl";

type Props = {
  onClick: () => void;
};

export function DrawButton({ onClick }: Props) {
  return (
    <motion.button
      style={{ backgroundColor: "white" }}
      className={className}
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
    >
      DRAW
    </motion.button>
  );
}
