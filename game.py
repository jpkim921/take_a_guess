from prompt_toolkit import prompt, PromptSession

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

    game_contract = None

    def __init__(self, game_contract, ante = 20):
        self.player_addr = None
        self.game_number = 0
        self.ante = ante # cost of play
        self.game_contract = game_contract

        # player object
        self.player = None

    
    def set_game_contract(self, game_address):
        if game_address == self.game_contract:
            print("Already set")
        else:
            self.game_contract = game_address

    def initiate_player(self):
        """
        Asks for player wallet address.
        Initiate player class with wallet and game contract address.
        Update player object with balance.
        """
        
        player_addr = prompt('Enter wallet address: ')
        # need to check and validate the address
        # if not valid then notify and re-prompt else move on
        try:
            
            player: Player = Player(game_addr=self.game_address)
            player.set_wallet_address(player_addr)
            player.update_self()
            self.player = player
        except Exception as e:
            print(f"Error: {e}")

        self.player_addr = player_addr
        print(f'You entered: \n\t\t{self.player_addr}')


    def start_game(self) -> bool:
        start = prompt("Ready? (Y/N) >>> ", validator=YesNoValidator())
        return start.lower() in ['y', 'yes']

    def win_round(self, user_guess: int, round_target: int) -> bool:
        return user_guess == round_target

    def round_payout(self, round: int):
        """
        player has won the game. pay/add payout for the round to player
        """
        amount = GuessGame.payout[round]
        print(f"AMOUNT WON IN ROUND {round}", amount)
        previous_player_bal = self.player.balance
        self.player.balance += amount
        new_player_bal = self.player.balance
        msg = f"""
            Previous Balance: {previous_player_bal}
        +          Round Win: {amount}
        --------------------------------------------
                              {new_player_bal} 
        """
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
            print("DEV - take ante")

            pass
        # pass




    def run(self):

        print("Welcome to the Guessing Game!")
        
        # ask for wallet address
        self.initiate_player()
        
        while True:
            try:
                # ask if ready to start
                # yes -> play_round; no -> keep asking if ready
                if self.start_game():
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



