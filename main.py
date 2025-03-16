import ecdsa
import hashlib
import json
import random
import base58  # Make sure to install this library: pip install base58

# Define the maximum possible private key value
MAX_PRIVATE_KEY = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140

def generate_private_key():
    # Generate a random private key within the valid range
    return random.randint(1, MAX_PRIVATE_KEY)

def private_key_to_wif(private_key):
    # Convert the private key to Wallet Import Format (WIF)
    private_key_bytes = private_key.to_bytes(32, byteorder='big')
    extended_key = b'\x80' + private_key_bytes
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]  # Fixed: Added missing parenthesis
    wif = extended_key + checksum
    return base58.b58encode(wif).decode('utf-8')

def private_key_to_address(private_key):
    # Derive the public key from the private key
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
    checksum = hashlib.sha256(hashlib.sha256(extended_hash).digest()).digest()[:4]  # Fixed: Added missing parenthesis
    binary_address = extended_hash + checksum
    
    # Convert to Base58
    return base58.b58encode(binary_address).decode('utf-8')

def generate_wallet(num_keys):
    wallet = []
    for _ in range(num_keys):
        private_key = generate_private_key()
        wif = private_key_to_wif(private_key)
        address = private_key_to_address(private_key)
        wallet.append({
            'private_key': hex(private_key),
            'wif': wif,
            'address': address
        })
    return wallet

def save_key_to_file(key_data, filename='wallet.json'):
    # Load existing data if the file exists
    try:
        with open(filename, 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []
    
    # Append the new key data
    existing_data.append(key_data)
    
    # Save the updated data back to the file
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=4)

def generate_and_save_keys(num_keys):
    for i in range(num_keys):
        private_key = generate_private_key()
        wif = private_key_to_wif(private_key)
        address = private_key_to_address(private_key)
        
        key_data = {
            'private_key': hex(private_key),
            'wif': wif,
            'address': address
        }
        
        # Save each key to the file as soon as it is generated
        save_key_to_file(key_data)
        print(f"Generated and saved key {i + 1}/{num_keys}")

if __name__ == "__main__":
    # Number of private keys to generate
    num_keys = 115792089237316195423570985008687907852837564279074904382605163141518161494336  # Max:115792089237316195423570985008687907852837564279074904382605163141518161494336
    # Generate and save the keys
    generate_and_save_keys(num_keys)
    
    print(f"Generated and saved {num_keys} private keys to wallet.json")
