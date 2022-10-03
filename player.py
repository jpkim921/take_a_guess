import sys
from prompt_toolkit import prompt, PromptSession
from web3 import Web3, EthereumTesterProvider

from generate_number import generate_guess
from validators import NumberValidator, NotStringValidator, YesNoValidator

class Player:

    def __init__(self, game_addr: str, wallet_addr=None):
        self.addr = wallet_addr
        self.balance = None
        self.game_addr = game_addr

        self.connect_game_contract(game_addr=self.game_addr)

    # def set_wallet_addr(self, addr):
    #     self.addr = addr

    # should make this into a decorator
    def update_self(self):
        self.balance = self.w3.eth.get_balance(self.addr)
        return self.addr, self.balance

    def connect_game_contract(self, game_addr):
        # self.game_addr = game_addr
        try:
            self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
            assert self.w3.isConnected()
            self.update_self()
        except Exception as e:
            print("Error - Player.connect_game_contract(self, game_addr): ", e)
    
    def get_game_ante(self):
        """get the ante amount from game contract"""
        """get it from contract or should the game class just apply it?(python)"""

    def pay_ante(self, ante_amount):
        # transfer ante to contract
        print(f"player paid {ante_amount}")

        

# wallet_address = "0xb5EeC83a336d28175Fc9F376420dceE865546451"
# game_contract = "0x97848eA083BB4f8F4dD095226f007Fa30d781316"
# player = Player(game_addr=game_contract, wallet_addr=wallet_address)

# print(player.balance)