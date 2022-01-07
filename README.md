# Blockchain with Python


## Introduction - Blockchain with Python <a name="intro"></a>

Your new startup is focusing on building a portfolio management system that supports not only traditional assets like gold, silver, stocks, etc, but crypto-assets as well! The problem is, there are so many coins out there! It's a good thing you understand how HD wallets work, since you'll need to build out a system that can create them. You're in a race to get to the market. There aren't as many tools available in Python for this sort of thing, yet.
Thankfully, you've found a command line tool, hd-wallet-derive that supports not only BIP32, BIP39, and BIP44, but
also supports non-standard derivation paths for the most popular wallets out there today! However, you need to integrate
the script into your backend with your dear old friend, Python.

We will start with generate the a mneumonic for a set of keys which we will turn into accounts to transfer coins between.

## Narrative of code <a name="para1"></a>

1. Using the following website, https://iancoleman.io/bip39/
2. Generate a 12 word mnemonics, making sure the "Coin" is selected for ETH. This will be used as the basis of address for moving ETH between accounts. Copy the 12 words into the .env and assign it to a constant called 'mnemonic'. 

<p align="center"><b>https://iancoleman.io/bip39/</b></p>
<p align="center">
  <img width="460" height="300" src="https://github.com/jayxcao/week19-homework/blob/main/Images/BIP39%20generate.PNG">
</p>


3. Using the mneumonic constant, generate the public, private keys and address for the exercise, limiting the accounts to 3. The following code will parse the mnewmonic and the coin (ETH).


```py
def derive_wallets(mnemonic,coin):
    command = ('php derive -g --mnemonic="{}" --cols=path,address,privkey,pubkey --format=json --coin={} --numderive=3').format(mnemonic,coin)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)
}
```

4. Expect an output of the following: 
<p align="center"><b>derive wallets</b></p>
<p align="center">
  <img width="460" src="https://github.com/jayxcao/week19-homework/blob/main/Images/step4output.PNG">
</p>

5. We now need to create an account from the private keys generated from above to start loading some faucet and transfer it between accounts. The following code turns the private key generated from the mneumonics into an account we can use. 

```py
def priv_key_to_account(coins,priv_key):
    if coins == ETH:
        return Account.privateKeyToAccount(priv_key)

eth_acc = priv_key_to_account(ETH, derive_wallets(mnemonic, ETH)[2]['privkey'])
```

6. It is now time to load some faucet (100ETH) into each account of the mneumonics, I have generated the same accounts in Ganache using localhost network as such:

<p align="center"><b>Ganache</b></p>
<p align="center">
  <img width="460" height="300" src="https://github.com/jayxcao/week19-homework/blob/main/Images/step6output.PNG">
</p>


7. Now we will need to create a transaction for ETH, the following code creates uses the web3 library for ethereum to call the parameters for a transaction. We're sending 11ETH from "0xf4dCe8041Cfeb9E493395738A3443491c08A1011" to "0xf4Ad3d8661C49D13113D1a656D943932521B4F3d"

```py
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

create_tx(ETH,eth_acc,"0xf4Ad3d8661C49D13113D1a656D943932521B4F3d", 11)
```

8. We commit to the transaction to the blockchain by using the send transaction function as below as this would output a transaction hash that we can trace in the blockchain.


```py
def send_tx(coins, account, to, amount):
    raw_tx = create_tx(coins, account, to, amount)
    if coin == ETH:
        signed_txn = eth_acc.sign_transaction(raw_tx)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(result.hex())
        return result.hex()

send_tx(ETH,eth_acc,"0xf4Ad3d8661C49D13113D1a656D943932521B4F3d", 11)
```

9. Transaction has been submitted to the blockchain:

insert pic
<p align="center"><b>Transaction on blockchain</b></p>
<p align="center">
  <img width="460" height="300" src="https://github.com/jayxcao/week19-homework/blob/main/Images/step9output.PNG">
</p>

