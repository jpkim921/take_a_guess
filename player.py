import sys
from prompt_toolkit import prompt, PromptSession
from web3 import Web3, EthereumTesterProvider

from generate_number import generate_guess
from validators import NumberValidator, NotStringValidator, YesNoValidator

# 0xb5EeC83a336d28175Fc9F376420dceE865546451
# 0x27f15096a283253760e0d89daa59b9e76e735f13a3f30191153def50b6f9fb94
# snap cushion afford outside field banana card almost visit punch remove bargain
class Player:

    def __init__(self):
        self.addr = None
        self.balance = None
        self.game_address = None


    def set_address(self, addr):
        self.addr = addr

    def update_self(self):
        print("update_self")


    def connect_game_contract(self, game_address):
        self.game_address = game_address
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        if w3.isConnected():
            self.update_self()
        

        pass


player = Player()
game_contract = "0x97848eA083BB4f8F4dD095226f007Fa30d781316"
player.connect_game_contract(game_contract)