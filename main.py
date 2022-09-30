import sys
from prompt_toolkit import prompt, PromptSession

from generate_number import generate_guess
from validators import NumberValidator

class Player:
    def __init__(self):
        self.addr = None


class GuessGame:
    def __init__(self, ante = 20):
        self.session = PromptSession()
        self.ante = ante
        self.addr = None
        
    # def prompt(self, prompt_text: str) -> str:
    #     try:
    #         input = prompt(prompt_text)
    #     except KeyboardInterrupt as e:
    #         print(e)
    #     except EOFError as e:
    #         print(e)

    #     return input

    def session_prompt(self, prompt_text: str) -> str:
        try:
            input = self.session.prompt(prompt_text)
            return input
        except KeyboardInterrupt as e:
            print(e)
        except EOFError as e:
            print(e)



    def prompt_for_wallet_address(self):
        addr = self.session_prompt('Enter wallet address: ')
        # need to check and validate the address
        # if not valid then notify and re-prompt else move on
        self.addr = addr
        print(f'You entered: \n\t\t{self.addr}')

    def start_game(self) -> bool:
        start = self.session_prompt("Ready? (Y/N) >>> ")
        print(start.lower())
        return start.lower() in ['y', 'yes']

    def start_round(self, round):
        print(f"Round {round} started.")

        # generate number for user to guess
        target = generate_guess(1, 2**round)
        print("target: ", target)
        print('generating guess...\n...\n...')
        print("guess generated")
        user_guess = int(prompt("Try a guess: "))
        print(f"You guessed {user_guess}")

        if user_guess == target:
            round += 1
            print('Good guess!')
            print('Moving on to next round...')
            return round
        # pass

    def main(self):

        print("Welcome to the Guessing Game!")
        
        # ask for wallet address
        self.prompt_for_wallet_address()
        
        while True:
            try:
                # ask if ready to start
                # yes -> start_round; no -> keep asking if ready
                if self.start_game():
                    curr_round = 1
                    while curr_round <= 5:
                        curr = self.start_round(round=curr_round)
                        if curr_round + 1 == curr:
                            curr_round = curr
                            print('DEV NOTE: move onto next round')
                        else:
                            print("you lose. try again.")
                            break
                        

            except KeyboardInterrupt:
                continue
            except EOFError:
                break
        
        # print('GoodBye!')

if __name__ == '__main__':
    g = GuessGame()
    g.main()
    print('GoodBye!')