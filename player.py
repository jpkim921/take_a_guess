import sys
from prompt_toolkit import prompt, PromptSession

from generate_number import generate_guess
from validators import NumberValidator, NotStringValidator, YesNoValidator

class Player:
    def __init__(self):
        self.addr = None
