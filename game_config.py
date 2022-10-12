from web3 import Web3
from web3.exceptions import InvalidAddress

import os
import json
import pprint
from pathlib import Path

pp = pprint.PrettyPrinter(indent=4)

class GameConfig:


    CONFIG_TEMPLATE = {
        "address"     : "Replace address in between quotes",
        "private_key" : "Replace pk in between quotes",
    }
    

    def __init__(self):
        pass

    def create_config_template(self, config_template: str = CONFIG_TEMPLATE, config_path: str = "./gg_config.json"):
        try:
            with open(config_path, 'w') as config:
                config.write(json.dumps(config_template))
        except Exception as e:
            print(f"Error: {e}")

    def read_config(self, config_path: str = "./gg_config.json"):
        with open(config_path, 'r') as config:
            config_r = json.loads(config.read())
            # pp.pprint(config_r)
            return config_r

    def ask_for_wallet_addr(self):
        user_address = input("Enter address: ")
        
        if not Web3.isAddress(user_address):
            raise InvalidAddress
        
        return user_address

    def get_config(self, config_path: str = "./gg_config.json"):
        """
        Get the players config file.
        """
        config_file = Path(config_path)    
        if config_file.is_file():
            print("Config file available")
        else:
            print(f"'{config_path}' not available. Please create a config.json")
            addr = self.ask_for_wallet_addr()
            self.CONFIG_TEMPLATE["address"] = addr
            self.create_config_template(config_path=config_path)

        config = self.read_config(config_path)
        pp.pprint(config)



# g: GameConfig = GameConfig()
# g.get_config()
# g.get_config("newone.json")