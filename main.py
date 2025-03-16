import ecdsa
import hashlib
import json
import random
import base58
import signal
import sys

# Define the maximum possible private key value
MAX_PRIVATE_KEY = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140

# File to save the wallet
WALLET_FILE = "wallet.json"

# Global variable to store the wallet data
wallet = []

def generate_private_key():
    """Generate a random private key within the valid range."""
    return random.randint(1, MAX_PRIVATE_KEY)

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
    print("\nCtrl+C detected. Saving wallet before exiting...")
    save_wallet()
    sys.exit(0)

def generate_wallet(num_keys):
    """Generate the specified number of keys and add them to the wallet."""
    global wallet
    for i in range(num_keys):
        private_key = generate_private_key()
        wif = private_key_to_wif(private_key)
        address = private_key_to_address(private_key)
        
        wallet.append({
            "private_key": hex(private_key),
            "wif": wif,
            "address": address
        })
        
        print(f"Generated key {i + 1}/{num_keys}: {address}")

if __name__ == "__main__":
    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Number of private keys to generate
    num_keys = int(input("Enter the number of keys to generate(MAX:115792089237316195423570985008687907852837564279074904382605163141518161494336): "))

    # Generate the wallet
    print(f"Generating {num_keys} keys...")
    generate_wallet(num_keys)

    # Save the wallet to the file
    save_wallet()
