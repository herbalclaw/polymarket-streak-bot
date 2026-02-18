#!/usr/bin/env python3
"""Check wallet balance and allowance on Polymarket."""

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
print("CHECKING WALLET BALANCE")
print("=" * 70)
print()

from src.config import Config
from py_clob_client.client import ClobClient

# Initialize client
clob_client = ClobClient(
    host=Config.CLOB_API,
    key=Config.PRIVATE_KEY,
    chain_id=Config.CHAIN_ID,
    signature_type=0,
)

creds = clob_client.create_or_derive_api_creds()
clob_client.set_api_creds(creds)

# Check balance
try:
    balance = clob_client.get_balance()
    print(f"Wallet Address: {Config.FUNDER_ADDRESS or 'Using private key address'}")
    print()
    print(f"USDC Balance: ${balance}")
    print()

    if balance < 5:
        print("=" * 70)
        print("INSUFFICIENT BALANCE!")
        print("=" * 70)
        print()
        print(f"You need at least $5 USDC to trade.")
        print(f"Current balance: ${balance}")
        print()
        print("TO FIX THIS:")
        print("1. Go to https://polymarket.com")
        print("2. Connect your wallet (0x910eEB450F7CaAa2e273B4E5261f88B84C55dBb0)")
        print("3. Deposit USDC to your Polymarket account")
        print("4. Or check if you have USDC on Polygon that needs to be deposited")
        print()
        print("The bot detected $49.97 in trades.json but this is just the")
        print("tracking balance, not actual USDC on the blockchain.")
    else:
        print("=" * 70)
        print("BALANCE OK!")
        print("=" * 70)
        print(f"You have ${balance} USDC available for trading.")

except Exception as e:
    print(f"Error checking balance: {e}")
    print()
    print("This wallet may not be set up on Polymarket yet.")
