import { Card, DiscardedCard } from "../../../client/cards";

type Props = {
  card: Card | DiscardedCard | "discard";
};

const className =
  "flex justify-center items-center text-center w-28 h-36 border-black border-2 rounded-2xl text-xl";

export function CardView({ card }: Props) {
  if (card === "discard") {
    return (
      <div
        style={{ backgroundColor: "white" }}
        className={
          "flex justify-center items-center text-center w-28 h-36 rounded-2xl text-xl"
        }
      >
        DISCARD PILE
      </div>
    );
  }
  switch (card.kind) {
    case "action":
      const content: { [A in (typeof card)["action"]]: string } = {
        draw_two: "DRAW TWO",
        reverse: "REVERSE",
        skip: "SKIP",
      };
      return (
        <div style={{ backgroundColor: card.color }} className={className}>
          <span className="bg-white border-black border-2 px-1 py-2 w-5/6">
            {content[card.action]}
          </span>
        </div>
      );
    case "discarded_wild":
      if (card.card.is_draw_four) {
        return (
          <div style={{ backgroundColor: card.color }} className={className}>
            <span className="bg-white border-black border-2 px-1 py-2 w-5/6">
              WILD DRAW FOUR
            </span>
          </div>
        );
      }
      return (
        <div style={{ backgroundColor: card.color }} className={className}>
          <span className="bg-white border-black border-2 px-1 py-2 w-5/6">
            WILD
          </span>
        </div>
      );
    case "number":
      return (
        <div style={{ backgroundColor: card.color }} className={className}>
          <span className="bg-white border-black border-2 px-3 py-2 text-7xl font-bold">
            {card.number}
          </span>
        </div>
      );
    case "wild":
      if (card.is_draw_four) {
        return (
          <div style={{ backgroundColor: "white" }} className={className}>
            WILD DRAW FOUR
          </div>
        );
      }
      return (
        <div style={{ backgroundColor: "white" }} className={className}>
          WILD
        </div>
      );
  }
}
