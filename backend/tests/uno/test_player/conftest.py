import pytest

from src.uno.avatars import get_random_avatar
from src.uno.player import Player


@pytest.fixture
def player() -> Player:
    return Player(get_random_avatar())
