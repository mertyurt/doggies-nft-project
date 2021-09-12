from typing import Hashable
from brownie import network, AdvancedCollectible
from metadata import sample_metadata
from scripts.helpful_scripts import get_breed
from pathlib import Path
import os
import requests
import json

def main():
  print('working on ' + network.show_active())
  advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
  number_of_tokens = advanced_collectible.tokenCounter()
  print(f'Number of tokens created {number_of_tokens}')
  write_metadata(number_of_tokens, advanced_collectible)

def write_metadata(number_of_tokens, nft_contract):
  for token_id in range(number_of_tokens):
    collectible_metadata = sample_metadata.metadata_template
    breed = get_breed(nft_contract.tokenIdToBreed(token_id))
    metadata_file_name = (
      f'./metadata/{network.show_active()}/' + str(token_id) + "-" + breed + ".json  "
    )
    if Path(metadata_file_name).exists():
      print(f'{metadata_file_name} already found!')
    else:
      print(f'creating metadata file {metadata_file_name}')
      collectible_metadata["name"] = get_breed(nft_contract.tokenIdToBreed(token_id))
      collectible_metadata["description"] = f'An adorable {collectible_metadata["name"]} pup.'
      image_to_upload = None
      if os.getenv("UPLOAD_IPFS") == "true":
        image_path = f"./img/{breed.lower().replace('_', '-')}.png"
        image_to_upload = upload_to_ipfs(image_path)
      collectible_metadata["image"] = image_to_upload
      with open(metadata_file_name, "w") as file:
        json.dump(collectible_metadata, file)
      if os.getenv("UPLOAD_IPFS") == "true":
        upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
  with Path(filepath).open("rb") as fp:
    image_binary = fp.read()
    ipfs_url = "http://localhost:5001"
    response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})
    ipfs_hash = response.json()["Hash"]
    filename = filepath.split("/")[-1:][0]
    uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
    print(uri)
    return uri
  return None