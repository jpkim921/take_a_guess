from guessing_game.generate_number import generate_round_one_guess



def test_generate_round_one_guess():
    assert generate_round_one_guess() in [1,2]