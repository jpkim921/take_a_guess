import sys
from prompt_toolkit import prompt, PromptSession
from web3 import Web3, EthereumTesterProvider

from generate_number import generate_guess
from validators import NumberValidator, NotStringValidator, YesNoValidator

class Player:

    def __init__(self, w3=None, game_addr: str=None, game_contract=None, wallet_addr=None):
        self.addr = wallet_addr
        self.balance = None
        self.w3 = w3
        self.game_addr = game_addr
        self.game_contract = game_contract

        self.set_player_account()
        # self.connect_game_contract(game_addr=self.game_addr)

    # def set_wallet_addr(self, addr):
    #     self.addr = addr

    # should make this into a decorator
    def update_self(self):
        self.balance = self.w3.eth.get_balance(self.addr)
        return self.addr, self.balance

    def set_player_account(self):
        try:
            self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545')) 
            # with open("config.json", "r") as f:
            #     data = json.load(f)
            self.private_key = '0x27f15096a283253760e0d89daa59b9e76e735f13a3f30191153def50b6f9fb94'

            wallet = self.w3.eth.account.from_key(self.private_key)
            self.public_address = wallet.address
            assert self.public_address == self.addr, "Player Addresses Do Not Match" 
        except Exception as e:
            print(e)            

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


    def pay_ante(self, _amount: int):
        private_key = input("Enter private key for wallet address: ").strip()
        # private_key = "0x27f15096a283253760e0d89daa59b9e76e735f13a3f30191153def50b6f9fb94"
 
        # get the nonce.  Prevents one from sending the transaction twice
        nonce = self.w3.eth.getTransactionCount(self.addr)

        #build a transaction in a dictionary
        initial_tx = {
            'nonce': nonce,
            'value': self.w3.toWei(_amount, 'wei'),
            'gas': 2000000,
            'gasPrice': self.w3.eth.gas_price
        }

        func_tx = self.game_contract.functions.payAnte().build_transaction(initial_tx)
        # print("func_tx: ", func_tx)
        tx = {**func_tx, 'to': self.game_contract.address}

        #sign the transaction
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
        # signed_tx = web3.eth.account.sign_transaction(tx, private_key1)

        #send transaction
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        #get transaction hash
        print("transaction hash: ", self.w3.toHex(tx_hash))

        
# wallet_address = "0xb5EeC83a336d28175Fc9F376420dceE865546451"
# game_contract = "0x97848eA083BB4f8F4dD095226f007Fa30d781316"
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
# player = Player(w3=w3,game_addr=game_contract, wallet_addr=wallet_address)
# player.update_self()
# print(player.balance)