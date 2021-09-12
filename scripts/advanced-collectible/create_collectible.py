from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import get_breed
import time

def main():
  dev = accounts.add(config['wallets']['from_key'])
  advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
  transaction = advanced_collectible.createCollectible("None", {"from": dev})
  transaction.wait(1)
  time.sleep(55)
  requestId = transaction.events['requestedCollectible']['requestId']
  token_id = advanced_collectible.requestIdToTokenId(requestId)
  breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
  print('Dog breed of tokenId {} is {}'.format(token_id, breed))