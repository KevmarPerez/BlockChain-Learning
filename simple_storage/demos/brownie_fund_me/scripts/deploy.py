from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helful_scripts import get_account

def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract

    # if we are in a persistent network like rinkeby , use associated address
    # otherwise, deploy mocks
    if network.show_active() != "development":
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_Feed"
        ]
    else:
        print(f"The active neetwork is {network.show_active()}")
        print("Deploting Mocks.....")
        mock_aggregator = MockC3Aggregator.deploy(18, 2000000000000000000, {"from": account})
        price_feed_address = mock_aggregator.address
        print("Mocks Deployed")
        
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account}, 
        publish_source=True)
    print(f"Contract depoyed to {fund_me.address}")

def main():
    deploy_fund_me()
    