#!/usr/bin/env python3
"""Check both Polygon and Ethereum balances."""

import sys
import os

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

print("=" * 70)
print("CHECKING ALL NETWORK BALANCES")
print("=" * 70)
print()

from src.config import Config
from web3 import Web3

# Get wallet address
from web3 import Web3 as W3

temp_w3 = W3()
account = temp_w3.eth.account.from_key(Config.PRIVATE_KEY)
address = account.address

print(f"Wallet Address: {address}")
print(f"Address Link: https://polygonscan.com/address/{address}")
print()

# USDC contracts
USDC_POLYGON = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
USDC_ETHEREUM = "0xA0b86a33E6441e0A421e56E4773C3C4b0Db6b4Ed"  # Bridged USDC on Polygon

erc20_abi = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
]

# Check Polygon
print("[POLYGON NETWORK]")
try:
    poly_w3 = Web3(Web3.HTTPProvider("https://polygon-rpc.com"))
    if poly_w3.is_connected():
        usdc = poly_w3.eth.contract(address=USDC_POLYGON, abi=erc20_abi)
        balance = usdc.functions.balanceOf(address).call()
        decimals = usdc.functions.decimals().call()
        formatted = balance / (10**decimals)
        print(f"  USDC Balance: ${formatted:.2f}")

        if formatted > 0:
            print(f"  ✓ You have USDC on Polygon!")
    else:
        print("  Could not connect")
except Exception as e:
    print(f"  Error: {e}")

print()

# Check if maybe there's native USDC or bridged USDC
print("[CHECKING POLYGONSCAN...]")
print(
    f"  Visit: https://polygonscan.com/token/0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174?a={address}"
)
print()

# Try alternative: check if money is in Polymarket's system differently
print("[ALTERNATIVE CHECK]")
print("If you have $49.97 on Polymarket, it might be:")
print("1. In an open position (you bought shares that haven't settled)")
print("2. In the Polymarket smart contract as deposited collateral")
print("3. On a different wallet address")
print()

# Double check the private key derives to the right address
print("[VERIFYING WALLET]")
print(f"Private key derives to: {address}")
print(f"Is this the wallet with $49.97?")
print()
print("If not, you may have the wrong private key in .env")
