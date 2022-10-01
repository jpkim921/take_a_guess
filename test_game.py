from .main import GuessGame

game = GuessGame()
def test_game_initialized():
    assert isinstance(game, GuessGame)