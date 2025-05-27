import random
import base58
import hashlib
import ecdsa
import json
import signal
import sys
import os

# Define the maximum possible private key value
MAX_PRIVATE_KEY = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140

# Files to save the wallet and all WIFs
WALLET_FILE = "wallet.json"
ALL_WIFS_FILE = "all.txt"  # Changed to .txt for plain text format

# Global variables to store the wallet data and all WIFs
wallet = []
all_wifs = []

def load_all_wifs():
    """Load all previously generated WIFs from all.txt."""
    global all_wifs
    if os.path.exists(ALL_WIFS_FILE):
        with open(ALL_WIFS_FILE, "r") as f:
            all_wifs = f.read().splitlines()  # Read WIFs as lines
    else:
        all_wifs = []

def save_all_wifs():
    """Save all WIFs to all.txt (one WIF per line)."""
    with open(ALL_WIFS_FILE, "w") as f:
        for wif in all_wifs:
            f.write(f"{wif}\n")  # Write each WIF on a new line
    print(f"\nAll WIFs saved to {ALL_WIFS_FILE}.")

def generate_private_key():
    """Generate a random private key within the valid range."""
    return random.randint(18e14a7b6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321724, MAX_PRIVATE_KEY)

def private_key_to_wif(private_key):
    """Convert the private key to Wallet Import Format (WIF)."""
    private_key_bytes = private_key.to_bytes(32, byteorder='big')
    extended_key = b'\x80' + private_key_bytes
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]  # Use .digest() to get bytes
    wif = extended_key + checksum
    return base58.b58encode(wif).decode('utf-8')

def private_key_to_address(private_key):
    """Derive the Bitcoin address from the private key."""
    sk = ecdsa.SigningKey.from_string(private_key.to_bytes(32, byteorder='big'), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()
    
    # Hash the public key to get the address
    sha256_bpk = hashlib.sha256(public_key).digest()  # Use .digest() to get bytes
    ripemd160_bpk = hashlib.new('ripemd160')
    ripemd160_bpk.update(sha256_bpk)
    hashed_public_key = ripemd160_bpk.digest()  # Use .digest() to get bytes
    
    # Add network byte and checksum
    network_byte = b'\x00'
    extended_hash = network_byte + hashed_public_key
    checksum = hashlib.sha256(hashlib.sha256(extended_hash).digest()).digest()[:4]  # Use .digest() to get bytes
    binary_address = extended_hash + checksum
    
    # Convert to Base58
    return base58.b58encode(binary_address).decode('utf-8')

def save_wallet():
    """Save the wallet data to the wallet.json file."""
    with open(WALLET_FILE, "w") as f:
        json.dump(wallet, f, indent=4)
    print(f"\nWallet saved to {WALLET_FILE}.")

def signal_handler(sig, frame):
    """Handle Ctrl+C interruption."""
    print("\nCtrl+C detected. Saving wallet and all WIFs before exiting...")
    save_wallet()
    save_all_wifs()
    sys.exit(0)

def generate_wallet(num_keys):
    """Generate the specified number of keys and add them to the wallet."""
    global wallet, all_wifs
    for i in range(num_keys):
        private_key = generate_private_key()
        wif = private_key_to_wif(private_key)
        address = private_key_to_address(private_key)

        # Add to wallet
        wallet.append({
            "private_key": hex(private_key),
            "wif": wif,
            "address": address
        })

        # Add to all WIFs
        all_wifs.append(wif)

        print(f"Generated key {i + 1}/{num_keys}: {address}")

if __name__ == "__main__":
    # Load all previously generated WIFs
    load_all_wifs()

    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Number of private keys to generate
    try:
        num_keys = int(input("Enter the number of keys to generate: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        sys.exit(1)

    # Generate the wallet
    print(f"Generating {num_keys} keys...")
    generate_wallet(num_keys)

    # Save the wallet and all WIFs
    save_wallet()
    save_all_wifs()
