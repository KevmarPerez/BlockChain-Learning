from brownie import MockV3Aggregator, network, accounts, config
from web3 import Web3

DECIMAL = 18
STARTING_VALUE = 2000

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deloying Mocks...")

    if len(MockV3Aggregator) <=0:
        mock_aggregator = MockV3Aggregator.deploy(
            DECIMAL,
            Web3.toWei(STARTING_VALUE, "ether"),
            {"from": get_account()}
        )
    print("Mocks Deployed to address!")