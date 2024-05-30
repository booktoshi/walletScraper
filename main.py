import json
import logging
import os
import requests

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class CollectionController:
    BASE_URL = "https://dogeturbo.ordinalswallet.com"

    def get_ordinals_wallet_inscriptions(self, address):
        url = f"{self.BASE_URL}/wallet/{address}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to fetch inscriptions. Status code: {response.status_code}")
            return {"inscriptions": []}

collection_stat = CollectionController()

def start():
    help_message = """
    Welcome to The Node Runners Inscription Tool!
Here are the commands you can use:

1. inscription <address> - Get all the inscriptions for the given address.

2. list <collection_name> <skip> <limit> - Get all the inscriptions for the given collection name.
   skip -> Number of inscriptions to be skipped from start
   limit -> Max number of inscription data per command, max allowed is 2000 to avoid timeout.

3. balance <address> - Get the wallet balance including bitcoin balance, inscriptions, and drc20.

4. stats <collection_name> - Get the stats for a given collection.
    """
    print(help_message)

def get_ordinals_wallet_inscriptions(address):
    result = collection_stat.get_ordinals_wallet_inscriptions(address)
    logger.info(f"Fetched data: {result}")  # Log fetched data
    inscription_ids = [inscription["id"] for inscription in result["inscriptions"]]
    logger.info(f"Extracted inscription IDs: {inscription_ids}")  # Log extracted IDs
    # Save the inscription IDs to a JSON file
    try:
        output_file = os.path.join(os.getcwd(), 'inscriptionIDs.json')
        with open(output_file, 'w') as f:
            json.dump(inscription_ids, f, indent=4)
        logger.info(f"The JSON file has been saved successfully as {output_file}")
    except Exception as e:
        logger.error(f"Failed to save the JSON file: {e}")

def main():
    while True:
        command = input("Enter a command (type 'help' for available commands, 'exit' to quit): ")
        if command == 'exit':
            break
        elif command == 'help':
            start()
        else:
            parts = command.split()
            if parts[0] == 'inscription' and len(parts) == 2:
                address = parts[1]
                get_ordinals_wallet_inscriptions(address)
            else:
                print("Invalid command. Type 'help' for available commands.")

if __name__ == "__main__":
    main()
