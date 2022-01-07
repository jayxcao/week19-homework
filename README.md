# Blockchain with Python


## Introduction - Machine Learning and Risk mitigation in Finance <a name="intro"></a>

The financial sector in which operates throughout the world as we know, is arguably the most predominant and most influential industry throughout.

As in any industry and any society, no matter how advanced or behind, there is always ways and opportunities to cheat the system, and gain and leverage mis-information or poor security & operations, in order for financial gain.

As the world evolves and technology advances, we see more and more cases of fraud and data theft within the financial sector each year, costing businesses, individuals, and the economy billions of dollars.

The Purpose of this project is to use and develope machine learning models to prove the importance and the effectiveness of this technology in the industry, and how it should be implemented across the board.

## Narrative of code <a name="para1"></a>

1. Using the following website, https://iancoleman.io/bip39/
2. Generate a 12 word mnemonics, making sure the "Coin" is selected for ETH. This will be used as the basis of address for moving ETH between accounts. Copy the 12 words into the .env and assign it to a constant called 'mnemonic'. 

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

4. Expect an output of the following: insert pic
<p align="center"><b>Confusion Matrix</b></p>
<p align="center">
  <img width="460" height="300" src="https://github.com/chirathlv/project2/blob/chirath/Images/cm_lr_clf.png">
</p>

5. We now need to create an account from the private keys generated from above to start loading some faucet and transfer it between accounts. The following code turns the private key generated from the mneumonics into an account we can use. 

```py
def priv_key_to_account(coins,priv_key):
    if coins == ETH:
        return Account.privateKeyToAccount(priv_key)

eth_acc = priv_key_to_account(ETH, derive_wallets(mnemonic, ETH)[2]['privkey'])
```

6. It is now time to load some faucet (100ETH) into each account of the mneumonics, I have generated the same accounts in Ganache using localhost network as such: insert pic

<p align="center"><b>Confusion Matrix</b></p>
<p align="center">
  <img width="460" height="300" src="https://github.com/chirathlv/project2/blob/chirath/Images/cm_lr_clf.png">
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
<p align="center"><b>Confusion Matrix</b></p>
<p align="center">
  <img width="460" height="300" src="https://github.com/chirathlv/project2/blob/chirath/Images/cm_lr_clf.png">
</p>

