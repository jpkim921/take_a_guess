from web3 import Web3
import json

ganache_url = 'http://127.0.0.1:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))
account_1 = '0x0a8426BD2Fc9A3e48Dc82545fF206d41330a948B'
private_key1 = '0x6e8990d6e7a4703ed270c96b394820f66e5a987c4da67f93d3929d12864ea9bc'
account_2 = '0xb5EeC83a336d28175Fc9F376420dceE865546451'
game_address = '0x97848eA083BB4f8F4dD095226f007Fa30d781316'

owner = "0x0a8426BD2Fc9A3e48Dc82545fF206d41330a948B"
owner_pk = "0x6e8990d6e7a4703ed270c96b394820f66e5a987c4da67f93d3929d12864ea9bc"

def connect_to_game_contract():
    with open('./house_abi.json') as f:
        data = json.load(f)
        game_contract = web3.eth.contract(address=game_address, abi=data['abi'])
        return game_contract

contract = connect_to_game_contract()


def get_balance(account):
    print(web3.eth.get_balance(account))

def send_eth(_to, _amount):
    #get the nonce.  Prevents one from sending the transaction twice
    nonce = web3.eth.getTransactionCount(account_1)

    #build a transaction in a dictionary
    initial_tx = {
        'nonce': nonce,
        'value': web3.toWei(_amount, 'wei'),
        'gas': 2000000,
        'gasPrice': web3.eth.gas_price
    }

    func_tx = contract.functions.payAnte().build_transaction(initial_tx)
    print("func_tx: ", func_tx)
    tx = {**func_tx, 'to': _to}

    #sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key1)
    # signed_tx = web3.eth.account.sign_transaction(tx, private_key1)

    #send transaction
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    #get transaction hash
    print(web3.toHex(tx_hash))


def get_player_balance(_player):
    bal = contract.functions.balances(_player).call()
    print(bal)
    return bal


def pay_player(_player, _amount):

    # if _amount == 0:
    #     _amount = get_player_balance(_player)
    #get the nonce.  Prevents one from sending the transaction twice
    nonce = web3.eth.getTransactionCount(owner)

    #build a transaction in a dictionary
    initial_tx = {
        'nonce': nonce,
        # 'value': web3.toWei(_amount, 'wei'),
        'gas': 2000000,
        'gasPrice': web3.eth.gas_price
    }

    func_tx = contract.functions.transferToPlayer(_player, _amount).build_transaction(initial_tx)
    # # print("func_tx: ", func_tx)
    # tx = {**func_tx, 'to': _player}
    # print(tx)

    # #sign the transaction
    signed_tx = web3.eth.account.sign_transaction(func_tx, owner_pk)

    # #send transaction
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    # #get transaction hash
    print(web3.toHex(tx_hash))


# get_balance(account_1)

# get_balance(game_address)

# send_eth(game_address, 20)

get_balance(game_address)
get_player_balance(account_2)

pay_player(account_2, 20)
# contract.functions.transferToPlayer(account_1, 13).call()

get_balance(game_address)