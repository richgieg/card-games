import random
from typing import Literal, TypedDict


class BearAvatar(TypedDict):
    emoji: Literal["🐻"]
    name: Literal["Bear"]


class CatAvatar(TypedDict):
    emoji: Literal["🐱"]
    name: Literal["Cat"]


class CowAvatar(TypedDict):
    emoji: Literal["🐮"]
    name: Literal["Cow"]


class DogAvatar(TypedDict):
    emoji: Literal["🐶"]
    name: Literal["Dog"]


class FoxAvatar(TypedDict):
    emoji: Literal["🦊"]
    name: Literal["Fox"]


class FrogAvatar(TypedDict):
    emoji: Literal["🐸"]
    name: Literal["Frog"]


class HamsterAvatar(TypedDict):
    emoji: Literal["🐹"]
    name: Literal["Hamster"]


class KoalaAvatar(TypedDict):
    emoji: Literal["🐨"]
    name: Literal["Koala"]


class LionAvatar(TypedDict):
    emoji: Literal["🦁"]
    name: Literal["Lion"]


class MonkeyAvatar(TypedDict):
    emoji: Literal["🐵"]
    name: Literal["Monkey"]


class MouseAvatar(TypedDict):
    emoji: Literal["🐭"]
    name: Literal["Mouse"]


class OwlAvatar(TypedDict):
    emoji: Literal["🦉"]
    name: Literal["Owl"]


class PandaAvatar(TypedDict):
    emoji: Literal["🐼"]
    name: Literal["Panda"]


class PigAvatar(TypedDict):
    emoji: Literal["🐷"]
    name: Literal["Pig"]


class RabbitAvatar(TypedDict):
    emoji: Literal["🐰"]
    name: Literal["Rabbit"]


class RaccoonAvatar(TypedDict):
    emoji: Literal["🦝"]
    name: Literal["Raccoon"]


class SnailAvatar(TypedDict):
    emoji: Literal["🐌"]
    name: Literal["Snail"]


class TigerAvatar(TypedDict):
    emoji: Literal["🐯"]
    name: Literal["Tiger"]


class UnicornAvatar(TypedDict):
    emoji: Literal["🦄"]
    name: Literal["Unicorn"]


class WolfAvatar(TypedDict):
    emoji: Literal["🐺"]
    name: Literal["Wolf"]


Avatar = (
    BearAvatar
    | CatAvatar
    | CowAvatar
    | DogAvatar
    | FoxAvatar
    | FrogAvatar
    | HamsterAvatar
    | KoalaAvatar
    | LionAvatar
    | MonkeyAvatar
    | MouseAvatar
    | OwlAvatar
    | PandaAvatar
    | PigAvatar
    | RabbitAvatar
    | RaccoonAvatar
    | SnailAvatar
    | TigerAvatar
    | UnicornAvatar
    | WolfAvatar
)


avatars: list[Avatar] = [
    BearAvatar(emoji="🐻", name="Bear"),
    CatAvatar(emoji="🐱", name="Cat"),
    CowAvatar(emoji="🐮", name="Cow"),
    DogAvatar(emoji="🐶", name="Dog"),
    FoxAvatar(emoji="🦊", name="Fox"),
    FrogAvatar(emoji="🐸", name="Frog"),
    HamsterAvatar(emoji="🐹", name="Hamster"),
    KoalaAvatar(emoji="🐨", name="Koala"),
    LionAvatar(emoji="🦁", name="Lion"),
    MonkeyAvatar(emoji="🐵", name="Monkey"),
    MouseAvatar(emoji="🐭", name="Mouse"),
    OwlAvatar(emoji="🦉", name="Owl"),
    PandaAvatar(emoji="🐼", name="Panda"),
    PigAvatar(emoji="🐷", name="Pig"),
    RabbitAvatar(emoji="🐰", name="Rabbit"),
    RaccoonAvatar(emoji="🦝", name="Raccoon"),
    SnailAvatar(emoji="🐌", name="Snail"),
    TigerAvatar(emoji="🐯", name="Tiger"),
    UnicornAvatar(emoji="🦄", name="Unicorn"),
    WolfAvatar(emoji="🐺", name="Wolf")
]


def get_random_avatar(used_avatars: list[Avatar] = []) -> Avatar:
    available_avatars = [a for a in avatars if a not in used_avatars]
    return random.choice(available_avatars)
