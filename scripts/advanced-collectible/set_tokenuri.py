from brownie import AdvancedCollectible, network, config, accounts
from scripts.helpful_scripts import get_breed

dog_metadata_dic = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def main():
  print("working on " + network.show_active())
  advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) -1]
  number_of_advanced_tokens = advanced_collectible.tokenCounter()
  print(f"The number of tokens deployed is: {number_of_advanced_tokens}" )
  for token_id in range(number_of_advanced_tokens):
    breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
    if not advanced_collectible.tokenURI(token_id).startswith("https://"):
      print(f"setting token uri of {token_id}")
      set_tokenURI(token_id, advanced_collectible, dog_metadata_dic[breed])
    else:
      print(f"we already set this token URI: {token_id}")

def set_tokenURI(token_id, nft_contract, tokenURI):
  dev = accounts.add(config["wallets"]["from_key"])
  nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
  print(f"view nft at here: {OPENSEA_FORMAT.format(nft_contract.address, token_id)}")
  print("wait up to 20 min. and refresh")