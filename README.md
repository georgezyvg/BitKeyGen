# BitKeyGen

BitKeyGen is a Python script that generates Bitcoin private keys, Wallet Import Format (WIF) keys, and corresponding Bitcoin addresses. Each generated key is saved to a `wallet.json` file for easy access and management.

## Features

- Generates random Bitcoin private keys within the valid range.
- Converts private keys to Wallet Import Format (WIF).
- Derives Bitcoin addresses from private keys.
- Saves each generated key (private key, WIF, and address) to a `wallet.json` file.
- Provides real-time progress feedback during key generation.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/HugoXOX3/BitKeyGen.git
   cd BitKeyGen
   ```

2. **Install Dependencies**:
   The script requires the `base58` library for encoding. Install it using pip:
   ```bash
   pip install base58
   ```

3. **Run the Script**:
   ```bash
   python main.py
   ```

## Usage

1. **Set the Number of Keys**:
   Open the `main.py` file and modify the `num_keys` variable to specify how many keys you want to generate. For example:
   ```python
   num_keys = 10  # Generate 10 keys(Maximum:115792089237316195423570985008687907852837564279074904382605163141518161494336
   ```

2. **Run the Script**:
   Execute the script:
   ```bash
   python main.py
   ```

3. **Check the Output**:
   The generated keys will be saved in the `wallet.json` file in the same directory. Each key will include:
   - `private_key`: The private key in hexadecimal format.
   - `wif`: The Wallet Import Format (WIF) key.
   - `address`: The Bitcoin address.

   Example `wallet.json`:
   ```json
   [
       {
           \"private_key\": \"0x1e2b3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f809\",
           \"wif\": \"5HueCGU8rMjxEXxiPuD5BDu1E8jMZ1G7fC2o5Y6f4h6Z\",
           \"address\": \"1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa\"
       },
       {
           \"private_key\": \"0x2f3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f8091b\",
           \"wif\": \"5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF\",
           \"address\": \"1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs\"
       }
   ]
   ```

## Example

To generate 5 Bitcoin private keys and save them to `wallet.json`:

1. Set `num_keys = 5` in `main.py`.
2. Run the script:
   ```bash
   python main.py
   ```
3. Check the `wallet.json` file for the generated keys.

## Security Notes

- **Private Keys**: Never share your private keys. Anyone with access to a private key can control the associated Bitcoin.
- **File Storage**: Ensure the `wallet.json` file is stored securely. Consider encrypting it or storing it in a secure location.
- **Use at Your Own Risk**: This script is for educational purposes only. Use it responsibly.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
