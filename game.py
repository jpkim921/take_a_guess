import json

from prompt_toolkit import prompt, PromptSession
from web3 import Web3

from game_config import GameConfig
from player import Player
from generate_number import generate_guess
from validators import NumberValidator, NotStringValidator, YesNoValidator

class GuessGame:

    payout = {
        1: 15,
        2: 35,
        3: 85,
        4: 175,
        5: 375,
    }

    game_contract_addr = None

    def __init__(self, game_contract_addr, owner=None, owner_pk=None, ante = 20):
        
        self.game_contract_addr = game_contract_addr
        self.game_contract = None
        
        # run game config script
        config = GameConfig(game_contract_addr).run_config()
        self.config = config.config

        self.owner = owner or '0x0a8426BD2Fc9A3e48Dc82545fF206d41330a948B'
        self.owner_pk = owner_pk or '0x6e8990d6e7a4703ed270c96b394820f66e5a987c4da67f93d3929d12864ea9bc'
        self.wallet_address = None
        self.game_number = 0
        self.ante = ante # cost of play
        

        self.current_total_winnings = 0
        self.current_game_winnings = 0


        # player object
        self.player: Player = None
        
        # web3 
        self.w3 = None
        self.connect_w3()
        self.connect_to_game_contract()

    def connect_w3(self):
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        assert self.w3.isConnected()

    def set_owner_account(self):
        try:
            self.private_key = '0x6e8990d6e7a4703ed270c96b394820f66e5a987c4da67f93d3929d12864ea9bc'
            self.wallet = self.w3.eth.account.from_key(self.private_key)
            self.owner = self.wallet.address
        except Exception as e:
            print(e)

    def connect_to_game_contract(self):
        with open('./house_abi.json') as f:
            data = json.load(f)
            self.game_contract = self.w3.eth.contract(address=self.game_contract_addr, abi=data['abi'])

    def set_game_contract(self, game_address):
        if game_address == self.game_contract_addr:
            print("Already set")
        else:
            self.game_contract_addr = game_address

    def initiate_player(self):
        """
        Asks for player wallet address.
        Initiate player class with wallet and game contract address.
        Update player object with balance.
        """
        
        # wallet_address = prompt('Enter wallet address: ') # use this when ready to move on from development
        # wallet_address = "0xb5EeC83a336d28175Fc9F376420dceE865546451" # hadcoded for developing
        wallet_address = self.config['address']

        try:            
            player: Player = Player(w3=self.w3, game_addr=self.game_contract_addr, game_contract=self.game_contract, wallet_addr=wallet_address)
            self.player = player
            print("Player Initiated: ")
        except Exception as e:
            print(f"Error - GuessGame.initiate_player(): {e}")

        # self.wallet_address = wallet_address
        # print(f'You entered: \n\t\t{self.wallet_address}')


    def start_game(self) -> bool:
        start = prompt("Ready? (Y/N) >>> ", validator=YesNoValidator())
        return start.lower() in ['y', 'yes']

    def win_round(self, user_guess: int, round_target: int) -> bool:
        return user_guess == round_target

    def get_player_balance(self, _player):
        bal = self.game_contract.functions.balances(_player).call()
        return bal

    def pay_player(self, _player, _amount):

        #get the nonce.  Prevents one from sending the transaction twice
        nonce = self.w3.eth.getTransactionCount(self.owner)

        #build a transaction in a dictionary
        initial_tx = {
            'nonce': nonce,
            # 'value': web3.toWei(_amount, 'wei'),
            'gas': 2000000,
            'gasPrice': self.w3.eth.gas_price
        }

        func_tx = self.game_contract.functions.transferToPlayer(_player, _amount).build_transaction(initial_tx)
        # # print("func_tx: ", func_tx)
        # tx = {**func_tx, 'to': _player}
        # print(tx)

        # #sign the transaction
        signed_tx = self.w3.eth.account.sign_transaction(func_tx, self.owner_pk)

        # #send transaction
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # #get transaction hash
        print(self.w3.toHex(tx_hash))
        print(f"Successfully paid {_player}: {_amount}")


    def round_payout(self, round: int):
        """
        player has won the game. pay/add payout for the round to player
        """
                 
        curr_total = self.current_total_winnings
        curr_game = self.current_game_winnings
        previous_player_bal = self.player.balance

        # amount won this round
        round_win = GuessGame.payout[round]
        print(f"AMOUNT WON IN ROUND {round}", round_win)

        curr_game += round_win
        curr_total += curr_game
        # curr_total += (curr_game + round_win)

        self.player.balance += round_win
        new_player_bal = self.player.balance

        msg = f"""
                Current Game: {curr_game}
        +          Round Win: {round_win}
        --------------------------------------------
               Current Total: {curr_total} 
        """
        
        self.current_game_winnings = curr_game
        self.current_total_winnings = curr_total

        print(msg)


    def play_round(self, round):
        print(f"Game {self.game_number} - Round {round} started.")

        # generate number for user to guess
        start = 1
        end = 2**round
        target = generate_guess(start, end)

        print("DEV - target: ", target)

        print('generating guess...')
        print("guess generated\n")

        # get user guess
        user_guess = int(prompt("Try a guess: ", validator=NotStringValidator()))
        print(f"You guessed {user_guess}")

        if self.win_round(user_guess, target):
            print("DEV - pay winning to escrow")
            self.round_payout(round)
            print('Good guess!')
            print('Moving on to next round...')
            
            # update to next round
            round += 1
            return round
        else:
            # lost. pay winnings up to now
            # winnings_so_far = self.current_game_winnings
            print(f"LOST: but won {self.current_game_winnings}")
            payout = self.current_game_winnings
            
            if payout <= 0:
                print('lost it all')
            else:
                payout = self.current_game_winnings
                print("============")
                print(payout)
                print(self.player.addr)
                print("============")
                self.pay_player(self.player.addr, payout)
            print("total payout: ", payout)
                
            
            print("DEV - take ante")

            pass
        # pass


    def player_profile(self):
        # update player instance before to display the latest info
        p_info = self.player.update_self()
        p_into_str = f"""
        Player -  
            Address: {p_info[0]}
            Balance: {p_info[1]}
        """
        return p_into_str



    def run(self):

        print("Welcome to the Guessing Game!")
        
        # ask for wallet address
        self.initiate_player()
        while True:
            
            print(self.player_profile())

            try:
                # ask if ready to start
                # yes -> play_round; no -> keep asking if ready
                if self.start_game():

                    # player pays ante
                    prev_game_contract_balance = self.game_contract.functions.gameBalance().call()

                    self.player.pay_ante(self.ante)

                    # check game_contract balance.
                    # i think the best would be to check for the paid ante event
                    post_game_contract_balance = self.game_contract.functions.gameBalance().call()

                    print('prev: ', prev_game_contract_balance)
                    print('post: ', post_game_contract_balance)
                    print('paid: ', post_game_contract_balance > prev_game_contract_balance)
                    
                    print(self.current_total_winnings)
                    self.current_total_winnings -= self.ante
                    print(self.current_total_winnings)

                    curr_round = 1
                    self.game_number += 1
                    while curr_round <= 5:
                        curr = self.play_round(round=curr_round)
                        if curr_round + 1 == curr:
                            curr_round = curr
                            print('DEV NOTE: win. move onto next round \n')
                        else:
                            print("You lose. Try again.")
                            break
                    # reset game winnings to 0 for next attempt
                    self.current_game_winnings = 0
                else:
                    continue
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
        # print('GoodBye!')



    # def prompt(self, prompt_text: str) -> str:
    #     try:
    #         input = prompt(prompt_text)
    #     except KeyboardInterrupt as e:
    #         print(e)
    #     except EOFError as e:
    #         print(e)

    #     return input

    # def session_prompt(self, prompt_text: str, validator: None) -> str:
    #     try:
    #         if validator:
    #             input = self.session.prompt(prompt_text, validator=validator())
    #         else:
    #             input = self.session.prompt(prompt_text)
    #         return input
    #     except KeyboardInterrupt as e:
    #         print(e)
    #     except EOFError as e:
    #         print(e)



