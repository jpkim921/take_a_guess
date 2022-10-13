from game import GuessGame
from game_config import GameConfig

def main():
    game_contract_addr = "0x97848eA083BB4f8F4dD095226f007Fa30d781316"
    g = GuessGame(game_contract_addr)
    g.run()


if __name__ == '__main__':
    main()    
    print('GoodBye!')