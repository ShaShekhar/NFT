from brownie import AIGenNFT
from scripts.utils import get_account
from web3 import Web3


def main():
    account = get_account()
    AINft = AIGenNFT[-1]
    # print(AINft.baseURI())
    create_tx = AINft.mintAINft["uint256"](
        20, {"from": account, "value": Web3.toWei(0.02, "ether")}
    )
    create_tx.wait(1)
    print("Successfully minted 20 apes.")
