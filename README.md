# BitKeyGen

**BitKeyGen** is a Python script that generates Bitcoin private keys, Wallet Import Format (WIF) keys, and corresponding Bitcoin addresses. It is designed for educational purposes, testing, and wallet creation. The program ensures that all keys are generated securely and saves them to a `wallet.json` file for easy management.

---

## Features

- **Random Key Generation**: Generates cryptographically secure Bitcoin private keys.
- **WIF Conversion**: Converts private keys into Wallet Import Format (WIF) for easy import into wallets.
- **Address Derivation**: Derives Bitcoin addresses from private keys using elliptic curve cryptography.
- **File Storage**: Saves generated keys to a `wallet.json` file for easy access and backup.
- **Graceful Interrupt Handling**: Saves the wallet even if the program is interrupted with `Ctrl+C`.

---

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

---

## Usage

1. **Set the Number of Keys**:
   When prompted, enter the number of keys you want to generate.

2. **Check the Output**:
   The generated keys will be saved in the `wallet.json` file in the same directory. Each key will include:
   - `private_key`: The private key in hexadecimal format.
   - `wif`: The Wallet Import Format (WIF) key.
   - `address`: The Bitcoin address.

3. **Interrupt Handling**:
   If you press `Ctrl+C`, the program will save the current state of the wallet to `wallet.json` before exiting.

---

## Example

### Input:
```
Enter the number of keys to generate: 5
```

### Output:
```
Generating 5 keys...
Generated key 1/5: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
Generated key 2/5: 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy
Generated key 3/5: bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq
Generated key 4/5: 1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs
Generated key 5/5: 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
Wallet saved to wallet.json.
```

### `wallet.json`:
```json
[
    {
        "private_key": "0x1e2b3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f809",
        "wif": "5HueCGU8rMjxEXxiPuD5BDu1E8jMZ1G7fC2o5Y6f4h6Z",
        "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    },
    {
        "private_key": "0x2f3c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f8091b",
        "wif": "5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF",
        "address": "1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs"
    }
]
```

---

## Security Notes

- **Private Keys**: Never share your private keys. Anyone with access to a private key can control the associated Bitcoin.
- **File Storage**: Ensure the `wallet.json` file is stored securely. Consider encrypting it or storing it in a secure location.
- **Use at Your Own Risk**: This script is for educational purposes only. Use it responsibly.

---

## Donations

If you find this project useful, consider supporting it with a Bitcoin donation:

**Bitcoin Address**: `bc1qt7a6vl28czf00vmuse9j7xwpyr7jjt83m2hljh`

[![Donate Bitcoin](https://img.shields.io/badge/Donate-Bitcoin-orange?logo=bitcoin)](bitcoin:bc1qt7a6vl28czf00vmuse9j7xwpyr7jjt83m2hljh)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
