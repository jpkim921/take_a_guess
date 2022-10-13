from web3 import Web3
from web3.exceptions import InvalidAddress

from typing import List
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
    

    def __init__(self, game_contract_address):
        self.config_template = GameConfig.CONFIG_TEMPLATE
        self.config_template['game_contract_address'] = game_contract_address
        self.config = None
        pass

    def get_config_files(self, path = ''):
        configs = sorted([str(p) for p in Path(path).glob("*_config.json")])
        if configs:
            return configs
        return


    def create_config_template(self, config_template: str = None, config_path: str = "./gg_config.json"):
        if config_template == None:
            config_template = self.config_template

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
        If config file doesn't exist, it will be created within this function.
        The config will be saved to self.config for Game instance to use.
        """
        config_file = Path(config_path)    
        if config_file.is_file():
            print("Config file available")
        else:
            print(f"'{config_path}' not available. Please create a config.json")
            addr = self.ask_for_wallet_addr()
            self.CONFIG_TEMPLATE["address"] = addr
            self.create_config_template(config_path=config_path)

        self.config = self.read_config(config_path)
        pp.pprint(self.config)


    def run_config(self):
        # get list of config files
        # if list is empty go directly to creating one
        # if not empty, display the list of configs and let player choose
        file_choice = None
        config_files = self.get_config_files()
        if config_files:
            print("Please choose config to use: ")
            for idx, file in enumerate(config_files):
                print(f"{idx+1}: {file}")

            file_choice = input("Enter number >>")
            self.get_config(config_files[file_choice-1])
            print(self.config)
        else:
            self.get_config()

        pass
    




g: GameConfig = GameConfig("0xgamecontract")
# g.get_config()
# g.get_config("newone_config.json")

g.run_config()
