import sys
from prompt_toolkit import prompt, PromptSession
from web3 import Web3, EthereumTesterProvider

from generate_number import generate_guess
from validators import NumberValidator, NotStringValidator, YesNoValidator

class Player:

    def __init__(self, game_addr, wallet_addr=None):
        self.addr = wallet_addr
        self.balance = None
        self.game_addr = game_addr

    def set_wallet_addr(self, addr):
        self.addr = addr

    # should make this into a decorator
    def update_self(self):
        print("update_self")
        self.balance = self.w3.eth.get_balance(self.addr)

    def connect_game_contract(self, game_address):
        self.game_address = game_address
        try:
            self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
            self.update_self()
        except Exception as e:
            print("Error: ", e)
    
    def get_game_ante(self):
        """get the ante amount from game contract"""
        """get it from contract or should the game class just apply it?(python)"""


# player = Player()
# player.set_wallet_address("0xb5EeC83a336d28175Fc9F376420dceE865546451")
# game_contract = "0x97848eA083BB4f8F4dD095226f007Fa30d781316"
# player.connect_game_contract(game_contract)