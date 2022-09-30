import random


def generate_guess(start: int , end: int) -> int:
    """
    returns the target for player to guess
    """
    return random.randint(start, end)




def test_generate_guess():
    input = {'start': 1, 'end': 2}
    assert generate_guess(**input) in [1,2], "guess should be 1 or 2"

    guess = generate_guess(1,4)
    assert guess >= 1 and guess <= 4, "guess should be between 1 and 4 inclusive"


test_generate_guess()