export type Color = "red" | "yellow" | "green" | "blue";

type NumberCard = {
  kind: "number";
  id: number;
  color: Color;
  number: number;
};

type Action = "draw_two" | "reverse" | "skip";

type ActionCard = {
  kind: "action";
  id: number;
  color: Color;
  action: Action;
};

type WildCard = {
  kind: "wild";
  id: number;
  is_draw_four: boolean;
};

type DiscardedWildCard = {
  kind: "discarded_wild";
  color: Color;
  card: WildCard;
};

export type Card = NumberCard | ActionCard | WildCard;
export type DiscardedCard = NumberCard | ActionCard | DiscardedWildCard;
