import sys
from prompt_toolkit import prompt, PromptSession

from generate_number import generate_guess
from validators import NumberValidator, NotStringValidator, YesNoValidator

class GuessGame:
    def __init__(self, ante = 20):
        self.session = PromptSession()
        self.ante = ante
        self.addr = None
        self.game_number = 0
        
    # def prompt(self, prompt_text: str) -> str:
    #     try:
    #         input = prompt(prompt_text)
    #     except KeyboardInterrupt as e:
    #         print(e)
    #     except EOFError as e:
    #         print(e)

    #     return input

    def session_prompt(self, prompt_text: str, validator: None) -> str:
        try:
            if validator:
                input = self.session.prompt(prompt_text, validator=validator())
            else:
                input = self.session.prompt(prompt_text)
            return input
        except KeyboardInterrupt as e:
            print(e)
        except EOFError as e:
            print(e)


    def prompt_for_wallet_address(self):
        addr = prompt('Enter wallet address: ')
        # need to check and validate the address
        # if not valid then notify and re-prompt else move on
        self.addr = addr
        print(f'You entered: \n\t\t{self.addr}')


    def start_game(self) -> bool:
        # start = self.session_prompt("Ready? (Y/N) >>> ", )
        start = prompt("Ready? (Y/N) >>> ", validator=YesNoValidator())
        return start.lower() in ['y', 'yes']


    def start_round(self, round):
        print(f"Game {self.game_number} - Round {round} started.")

        # generate number for user to guess
        start = 1
        end = 2**round
        target = generate_guess(start, end)

        print("DEV - target: ", target)

        print('generating guess...')
        print("guess generated\n")
        user_guess = int(prompt("Try a guess: ", validator=NotStringValidator()))
        print(f"You guessed {user_guess}")

        if user_guess == target:
            round += 1
            print('Good guess!')
            print('Moving on to next round...')
            return round
        # pass

    def run(self):

        print("Welcome to the Guessing Game!")
        
        # ask for wallet address
        self.prompt_for_wallet_address()
        
        while True:
            try:
                # ask if ready to start
                # yes -> start_round; no -> keep asking if ready
                if self.start_game():
                    curr_round = 1
                    self.game_number += 1
                    while curr_round <= 5:
                        curr = self.start_round(round=curr_round)
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
