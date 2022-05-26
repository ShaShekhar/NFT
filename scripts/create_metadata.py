from pathlib import Path
from importlib_metadata import files
import requests, json, glob, os

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"

headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
}

IMAGE_FOLDER = "../ai-apes/*"
NUM_TO_UPLOAD = 20

images = glob.glob(IMAGE_FOLDER + ".png")
jsons = glob.glob(IMAGE_FOLDER + ".json")
images.sort()
jsons.sort()

TOKEN_URI = {}


def main():
    for token_id in range(NUM_TO_UPLOAD):
        metadata_file_name = f"../uploaded-json/{token_id}.json"
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            # ipfs_hash = upload_to_ipfs(img_path)
            ipfs_hash = upload_to_pinata(images[token_id], token_id, ".png")
            with open(jsons[token_id], "r") as f:
                collectible_metadata = json.load(f)

            collectible_metadata["image"] = "ipfs://" + ipfs_hash
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            json_hash = upload_to_pinata(metadata_file_name, token_id, ".json")
            TOKEN_URI[token_id] = "ipfs://" + json_hash

    with open("token_uri.json", "w") as f:
        json.dump(TOKEN_URI, f)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        img_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files=img_binary)
        return response.json()["Hash"]


def upload_to_pinata(filepath, token_id, ext):
    filename = str(token_id) + ext

    with Path(filepath).open("rb") as fp:
        file_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, file_binary)},
            headers=headers,
        )
    print(f"[INFO]: FILE UPLOADED.")
    return response.json()["IpfsHash"]


if __name__ == "__main__":
    main()
