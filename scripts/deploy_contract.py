from scripts.utils import get_account
from brownie import AIGenNFT


def deploy_contract():
    account = get_account()
    print(account)
    AINft = AIGenNFT[-1]
    base_uri = "ipfs://QmTDmNp7heiYEXKSLvAZuykzxGRNfLyPrFWaddzRmgSTSi/"
    # AIGenNFT.deploy(base_uri, {"from": account})
    create_tx = AINft.setBaseURI(base_uri, {"from": account})
    create_tx.wait(1)
    print("Successfully updated the baseURI")


def main():
    deploy_contract()


# brownie run scripts/deploy_contract.py --network rinkeby
