from typing import Literal

from pydantic import BaseModel

from enum import Enum


class Color(Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"


class NumberCard(BaseModel):
    kind: Literal["number"]
    id: int
    color: Color
    number: int

    def __init__(self, id: int, color: Color, number: int):
        super().__init__(kind="number", id=id, color=color, number=number)


class Action(Enum):
    DRAW_TWO = "draw_two"
    REVERSE = "reverse"
    SKIP = "skip"


class ActionCard(BaseModel):
    kind: Literal["action"]
    id: int
    color: Color
    action: Action

    def __init__(self, id: int, color: Color, action: Action):
        super().__init__(kind="action", id=id, color=color, action=action)


class WildCard(BaseModel):
    kind: Literal["wild"]
    id: int
    is_draw_four: bool

    def __init__(self, id: int, is_draw_four: bool):
        super().__init__(kind="wild", id=id, is_draw_four=is_draw_four)


class DiscardedWildCard(BaseModel):
    kind: Literal["discarded_wild"]
    color: Color
    card: WildCard

    def __init__(self, color: Color, card: WildCard):
        super().__init__(kind="discarded_wild", color=color, card=card)


Card = NumberCard | ActionCard | WildCard
DiscardedCard = NumberCard | ActionCard | DiscardedWildCard


cards: list[Card] = [
    NumberCard(0, Color.BLUE, 0),
    NumberCard(1, Color.BLUE, 1),
    NumberCard(2, Color.BLUE, 1),
    NumberCard(3, Color.BLUE, 2),
    NumberCard(4, Color.BLUE, 2),
    NumberCard(5, Color.BLUE, 3),
    NumberCard(6, Color.BLUE, 3),
    NumberCard(7, Color.BLUE, 4),
    NumberCard(8, Color.BLUE, 4),
    NumberCard(9, Color.BLUE, 5),
    NumberCard(10, Color.BLUE, 5),
    NumberCard(11, Color.BLUE, 6),
    NumberCard(12, Color.BLUE, 6),
    NumberCard(13, Color.BLUE, 7),
    NumberCard(14, Color.BLUE, 7),
    NumberCard(15, Color.BLUE, 8),
    NumberCard(16, Color.BLUE, 8),
    NumberCard(17, Color.BLUE, 9),
    NumberCard(18, Color.BLUE, 9),
    ActionCard(19, Color.BLUE, Action.DRAW_TWO),
    ActionCard(20, Color.BLUE, Action.DRAW_TWO),
    ActionCard(21, Color.BLUE, Action.REVERSE),
    ActionCard(22, Color.BLUE, Action.REVERSE),
    ActionCard(23, Color.BLUE, Action.SKIP),
    ActionCard(24, Color.BLUE, Action.SKIP),
    NumberCard(25, Color.GREEN, 0),
    NumberCard(26, Color.GREEN, 1),
    NumberCard(27, Color.GREEN, 1),
    NumberCard(28, Color.GREEN, 2),
    NumberCard(29, Color.GREEN, 2),
    NumberCard(30, Color.GREEN, 3),
    NumberCard(31, Color.GREEN, 3),
    NumberCard(32, Color.GREEN, 4),
    NumberCard(33, Color.GREEN, 4),
    NumberCard(34, Color.GREEN, 5),
    NumberCard(35, Color.GREEN, 5),
    NumberCard(36, Color.GREEN, 6),
    NumberCard(37, Color.GREEN, 6),
    NumberCard(38, Color.GREEN, 7),
    NumberCard(39, Color.GREEN, 7),
    NumberCard(40, Color.GREEN, 8),
    NumberCard(41, Color.GREEN, 8),
    NumberCard(42, Color.GREEN, 9),
    NumberCard(43, Color.GREEN, 9),
    ActionCard(44, Color.GREEN, Action.DRAW_TWO),
    ActionCard(45, Color.GREEN, Action.DRAW_TWO),
    ActionCard(46, Color.GREEN, Action.REVERSE),
    ActionCard(47, Color.GREEN, Action.REVERSE),
    ActionCard(48, Color.GREEN, Action.SKIP),
    ActionCard(49, Color.GREEN, Action.SKIP),
    NumberCard(50, Color.RED, 0),
    NumberCard(51, Color.RED, 1),
    NumberCard(52, Color.RED, 1),
    NumberCard(53, Color.RED, 2),
    NumberCard(54, Color.RED, 2),
    NumberCard(55, Color.RED, 3),
    NumberCard(56, Color.RED, 3),
    NumberCard(57, Color.RED, 4),
    NumberCard(58, Color.RED, 4),
    NumberCard(59, Color.RED, 5),
    NumberCard(60, Color.RED, 5),
    NumberCard(61, Color.RED, 6),
    NumberCard(62, Color.RED, 6),
    NumberCard(63, Color.RED, 7),
    NumberCard(64, Color.RED, 7),
    NumberCard(65, Color.RED, 8),
    NumberCard(66, Color.RED, 8),
    NumberCard(67, Color.RED, 9),
    NumberCard(68, Color.RED, 9),
    ActionCard(69, Color.RED, Action.DRAW_TWO),
    ActionCard(70, Color.RED, Action.DRAW_TWO),
    ActionCard(71, Color.RED, Action.REVERSE),
    ActionCard(72, Color.RED, Action.REVERSE),
    ActionCard(73, Color.RED, Action.SKIP),
    ActionCard(74, Color.RED, Action.SKIP),
    NumberCard(75, Color.YELLOW, 0),
    NumberCard(76, Color.YELLOW, 1),
    NumberCard(77, Color.YELLOW, 1),
    NumberCard(78, Color.YELLOW, 2),
    NumberCard(79, Color.YELLOW, 2),
    NumberCard(80, Color.YELLOW, 3),
    NumberCard(81, Color.YELLOW, 3),
    NumberCard(82, Color.YELLOW, 4),
    NumberCard(83, Color.YELLOW, 4),
    NumberCard(84, Color.YELLOW, 5),
    NumberCard(85, Color.YELLOW, 5),
    NumberCard(86, Color.YELLOW, 6),
    NumberCard(87, Color.YELLOW, 6),
    NumberCard(88, Color.YELLOW, 7),
    NumberCard(89, Color.YELLOW, 7),
    NumberCard(90, Color.YELLOW, 8),
    NumberCard(91, Color.YELLOW, 8),
    NumberCard(92, Color.YELLOW, 9),
    NumberCard(93, Color.YELLOW, 9),
    ActionCard(94, Color.YELLOW, Action.DRAW_TWO),
    ActionCard(95, Color.YELLOW, Action.DRAW_TWO),
    ActionCard(96, Color.YELLOW, Action.REVERSE),
    ActionCard(97, Color.YELLOW, Action.REVERSE),
    ActionCard(98, Color.YELLOW, Action.SKIP),
    ActionCard(99, Color.YELLOW, Action.SKIP),
    WildCard(100, False),
    WildCard(101, False),
    WildCard(102, False),
    WildCard(103, False),
    WildCard(104, True),
    WildCard(105, True),
    WildCard(106, True),
    WildCard(107, True),
]
