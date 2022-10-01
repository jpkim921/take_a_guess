import sys
from prompt_toolkit import prompt, PromptSession

from generate_number import generate_guess
from validators import NumberValidator, NotStringValidator, YesNoValidator

class Player:
    def __init__(self):
        self.addr = None
        self.balance = 0


    def set_address(self, addr):
        self.addr = addr
