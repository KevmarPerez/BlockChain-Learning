from brownie import MockV3Aggregator, network, accounts, config
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMAL = 8
STARTING_VALUE = 200000000000

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deloying Mocks...")

    if len(MockV3Aggregator) <=0:
        mock_aggregator = MockV3Aggregator.deploy(
            DECIMAL,
            STARTING_VALUE,
            {"from": get_account()}
        )
    print("Mocks Deployed to address!")