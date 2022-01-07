# Import dependencies
import subprocess
import json
from dotenv import load_dotenv


# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constants import *
import bit
from web3 import Web3, middleware, Account
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware
 
 
# Create a function called `derive_wallets`
def derive_wallets(mnemonic,coin):
    command = ('php derive -g --mnemonic="{}" --cols=path,address,privkey,pubkey --format=json --coin={} --numderive=3').format(mnemonic,coin)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
btc_dict = {}
btc_test_dict = {}
eth_acc = {}

#btc_coins = derive_wallets(mnemonic,BTC)
#btc_test_coins = derive_wallets(mnemonic,BTCTEST)



# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coins,priv_key):
    if coins == ETH:
        return Account.privateKeyToAccount(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coins, account, to, amount):
    if coins == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from":eth_acc.address, "to":to, "value": amount}
        )
        return {
            "from": eth_acc.address,
            "to": to,
            "value": amount,
            "gas": gasEstimate,
            "gasPrice": w3.eth.gasPrice,
            "nonce": w3.eth.getTransactionCount(eth_acc.address),
            #"chainID" : 5777
        }

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coins, account, to, amount):
    raw_tx = create_tx(coins, account, to, amount)
    if coin == ETH:
        signed_txn = eth_acc.sign_transaction(raw_tx)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(result.hex())
        return result.hex()


    
    
    
#Running functions 
eth_acc = {}
eth_coins = derive_wallets(mnemonic,ETH)
print(eth_coins)

#creating a ETH account with the last address from the derived wallets created above
eth_acc = priv_key_to_account(ETH, derive_wallets(mnemonic, ETH)[2]['privkey'])

print(eth_acc)

#Creating a transaction for the block from the eth_acc to the account specified with 120000 ETH
create_tx(ETH,eth_acc,"0x62e0ce2026f17dfCa91f3eA3ad1B890312df06AF", 12)

#commits the transactions to the blockchain from the eth_acc to the account specified with 120000 ETH
send_tx(ETH,eth_acc,"0x62e0ce2026f17dfCa91f3eA3ad1B890312df06AF", 12)