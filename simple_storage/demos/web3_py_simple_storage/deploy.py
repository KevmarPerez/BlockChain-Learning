from solcx import compile_standard, install_solc
import json, os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")

# reading the sol file
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# compile the solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0xafa8ab946706427aF9dbc55B20fA390e222d6bC3"
# private_key = "0x8b02b0bed02670f574944bce730d80fa174cf86c3c0f892f9ec6dd2a8e0abec5"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# # get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# send a transaction
transaction = SimpleStorage.constructor().buildTransaction({
    "gasPrice": w3.eth.gas_price,
    "chainId":chain_id, 
    "from":my_address, 
    "nonce":nonce
})

# sign a tranaction, 
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# build the transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# working with the contract
# contract address
# contract abi

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call => simulates making a cal and getting  a state value
# transact -> actually  making a state change

# initial value of favorite number
print(simple_storage.functions.retrieve().call())
# print(simple_storage.functions.store(15).call())

store_transaction = simple_storage.functions.store(15).build_transaction({
    "gasPrice": w3.eth.gas_price,
    "chainId":chain_id, 
    "from":my_address, 
    "nonce":nonce+1
})

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call())