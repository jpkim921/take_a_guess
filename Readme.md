# Take a Guess

CLI app that takes a simple 'guess the numbers' game and uses a smart contract as a way to pay Ether both ways.

Mainly used this to review python and solidity as well as use web3py to interact with the smart contract.

If you have Ganache, start it up with the seed phrase below and it should work. Once I get the logic more correct in terms of figuring out the payout and clean the code up a lot, I'll deploy to a testnet and let it run and live there.
Can always add config.json or similar style to connect to any instance of the house contract and players wallet.


# console library
 - prompt_toolkit -> using this one

# game contract
 - address: 0x97848eA083BB4f8F4dD095226f007Fa30d781316

# ganache
 - owner: 0x0a8426BD2Fc9A3e48Dc82545fF206d41330a948B
 - owner_pk: 0x6e8990d6e7a4703ed270c96b394820f66e5a987c4da67f93d3929d12864ea9bc
 - player addr: 0xb5EeC83a336d28175Fc9F376420dceE865546451
 - player pk: 0x27f15096a283253760e0d89daa59b9e76e735f13a3f30191153def50b6f9fb94
 - ganache mnemonic: snap cushion afford outside field banana card almost visit punch remove bargain
 - ganache -m "snap cushion afford outside field banana card almost visit punch remove bargain"