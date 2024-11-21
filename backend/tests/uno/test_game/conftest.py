import pytest

from src.uno.game import Game


@pytest.fixture
def game() -> Game:
    return Game()
