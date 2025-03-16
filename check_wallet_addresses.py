import requests
import json

# Bitcoin Explorer API endpoint
BITCOIN_EXPLORER_API_URL = "https://bitcoinexplorer.org/api"

# Input and output files
WALLET_FILE = "wallet.json"  # File containing generated addresses
OUTPUT_FILE = "found.txt"    # File to save addresses with transactions

def check_address_transactions(address):
    """
    Check if a Bitcoin address has any transactions using the Bitcoin Explorer API.
    """
    url = f"{BITCOIN_EXPLORER_API_URL}/address/{address}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Check if the address has any transactions
        if data.get("chain_stats", {}).get("tx_count", 0) > 0:
            return True
    except requests.exceptions.RequestException as e:
        print(f"Error checking address {address}: {e}")
    return False

def save_found_address(address):
    """
    Save the address to the found.txt file.
    """
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"{address}\n")

def load_wallet_addresses(wallet_file):
    """
    Load Bitcoin addresses from the wallet.json file.
    """
    with open(wallet_file, "r") as f:
        wallet_data = json.load(f)
    return [entry["address"] for entry in wallet_data]

def main():
    # Load addresses from wallet.json
    addresses_to_check = load_wallet_addresses(WALLET_FILE)
    print(f"Loaded {len(addresses_to_check)} addresses from {WALLET_FILE}.")

    for address in addresses_to_check:
        print(f"Checking address: {address}")
        if check_address_transactions(address):
            print(f"Address {address} has transactions. Saving to found.txt.")
            save_found_address(address)
        else:
            print(f"Address {address} has no transactions.")

if __name__ == "__main__":
    main()
