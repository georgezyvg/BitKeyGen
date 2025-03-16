import requests
import json
import concurrent.futures

# API endpoints
MEMPOOL_API_URL = "https://mempool.space/api/address/{address}"
BTCSCAN_API_URL = "https://api.btcscan.org/api/address/{address}"
BITCOIN_EXPLORER_API_URL = "https://bitcoinexplorer.org/api/address/{address}"

# Input and output files
WALLET_FILE = "wallet.json"  # File containing generated addresses
OUTPUT_FILE = "found.txt"    # File to save addresses with transactions

def check_address_transactions(address):
    """
    Check if a Bitcoin address has any transactions using multiple APIs.
    """
    # Try Mempool.space API first
    try:
        response = requests.get(MEMPOOL_API_URL.format(address=address))
        response.raise_for_status()
        data = response.json()
        if data.get("chain_stats", {}).get("tx_count", 0) > 0:
            return True
    except requests.exceptions.RequestException:
        pass  # Fallback to BTCScan API if Mempool.space fails

    # Try BTCScan API as a fallback
    try:
        response = requests.get(BTCSCAN_API_URL.format(address=address))
        response.raise_for_status()
        data = response.json()
        if data.get("tx_count", 0) > 0:
            return True
    except requests.exceptions.RequestException:
        pass  # Fallback to Bitcoin Explorer API if BTCScan fails

    # Try Bitcoin Explorer API as a final fallback
    try:
        response = requests.get(BITCOIN_EXPLORER_API_URL.format(address=address))
        response.raise_for_status()
        data = response.json()
        if data.get("chain_stats", {}).get("tx_count", 0) > 0:
            return True
    except requests.exceptions.RequestException:
        pass  # Address has no transactions or all APIs failed

    return False

def save_found_address(address, wif):
    """
    Save the address and WIF to the found.txt file.
    """
    with open(OUTPUT_FILE, "a") as f:
        f.write(f"Address: {address}, WIF: {wif}\n")

def load_wallet_data(wallet_file):
    """
    Load Bitcoin addresses and WIFs from the wallet.json file.
    """
    with open(wallet_file, "r") as f:
        wallet_data = json.load(f)
    return wallet_data  # List of dictionaries containing "address" and "wif"

def check_addresses_parallel(wallet_data):
    """
    Check addresses in parallel using multiple threads.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_address = {executor.submit(check_address_transactions, entry["address"]): entry for entry in wallet_data}
        for future in concurrent.futures.as_completed(future_to_address):
            entry = future_to_address[future]
            address = entry["address"]
            wif = entry["wif"]
            try:
                if future.result():
                    print(f"Address {address} has transactions. Saving to found.txt.")
                    save_found_address(address, wif)
                else:
                    print(f"Address {address} has no transactions.")
            except Exception as e:
                print(f"Error checking address {address}: {e}")

def main():
    # Load wallet data from wallet.json
    wallet_data = load_wallet_data(WALLET_FILE)
    print(f"Loaded {len(wallet_data)} addresses from {WALLET_FILE}.")

    # Check addresses in parallel
    check_addresses_parallel(wallet_data)

if __name__ == "__main__":
    main()
