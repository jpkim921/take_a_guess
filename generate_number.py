import random


def generate_guess(start: int, end: int) -> int:
    """
    returns the target number for player to guess
    """
    # print(f"Target is between {start} and {end}\n")
    return random.randint(start, end)


def test_generate_guess():
    input = {'start': 1, 'end': 2}
    assert generate_guess(**input) in [1,2], "guess should be 1 or 2"

    guess = generate_guess(1,4)
    assert guess >= 1 and guess <= 4, "guess should be between 1 and 4 inclusive"

# print("start - testing generate guess")
test_generate_guess()
# print("end - testing generate guess\n")