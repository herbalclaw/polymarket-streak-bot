#!/usr/bin/env python3
"""Check USDC balance on Polygon."""

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
print("CHECKING POLYGON WALLET BALANCE")
print("=" * 70)
print()

from src.config import Config
from web3 import Web3

# Connect to Polygon
polygon_rpc = "https://polygon-rpc.com"
w3 = Web3(Web3.HTTPProvider(polygon_rpc))

if not w3.is_connected():
    print("[FAIL] Cannot connect to Polygon network")
    sys.exit(1)

print("[OK] Connected to Polygon")
print()

# Get wallet address from private key
account = w3.eth.account.from_key(Config.PRIVATE_KEY)
address = account.address

print(f"Wallet Address: {address}")
print()

# Check MATIC balance
matic_balance = w3.eth.get_balance(address)
matic_balance_eth = w3.from_wei(matic_balance, "ether")
print(f"MATIC Balance: {matic_balance_eth:.4f} MATIC")

# USDC contract on Polygon
usdc_contract = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
usdc_abi = [
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

# Check USDC balance
usdc = w3.eth.contract(address=usdc_contract, abi=usdc_abi)
usdc_balance = usdc.functions.balanceOf(address).call()
decimals = usdc.functions.decimals().call()
usdc_balance_formatted = usdc_balance / (10**decimals)

print(f"USDC Balance: ${usdc_balance_formatted:.2f}")
print()

if usdc_balance_formatted < 5:
    print("=" * 70)
    print("INSUFFICIENT USDC BALANCE!")
    print("=" * 70)
    print()
    print("You need at least $5 USDC on Polygon to trade on Polymarket.")
    print()
    print("TO FIX THIS:")
    print("1. Go to https://polymarket.com")
    print("2. Connect your wallet")
    print("3. Click 'Deposit' and add USDC")
    print("4. The USDC will be deposited to the Polymarket exchange")
    print()
    print("OR if you have USDC elsewhere:")
    print("- Bridge USDC to Polygon network")
    print("- Then deposit to Polymarket")
    print()
    print(f"Current balance: ${usdc_balance_formatted:.2f} USDC")
    print()
    print("NOTE: The $49.97 in trades.json is just the bot's tracking")
    print("      balance, not actual USDC in your wallet.")
else:
    print("=" * 70)
    print("BALANCE OK!")
    print("=" * 70)
    print(f"You have ${usdc_balance_formatted:.2f} USDC available.")
    print()
    print("However, you still need to deposit this to Polymarket.")
    print("Go to https://polymarket.com and click 'Deposit'")
