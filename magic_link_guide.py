#!/usr/bin/env python3
"""Find the correct Magic Link wallet setup."""

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
print("MAGIC LINK WALLET SETUP GUIDE")
print("=" * 70)
print()

from src.config import Config
from web3 import Web3

print("CURRENT SETUP:")
print(f"  Private Key: {Config.PRIVATE_KEY[:20]}...")

# What address does the private key control?
w3 = Web3()
account = w3.eth.account.from_key(Config.PRIVATE_KEY)
signing_address = account.address

print(f"  Signing Address: {signing_address}")
print(f"  Funder Address: {Config.FUNDER_ADDRESS}")
print(f"  Signature Type: {Config.SIGNATURE_TYPE}")
print()

print("=" * 70)
print("THE PROBLEM")
print("=" * 70)
print()
print("Magic Link wallets work differently than MetaMask:")
print()
print("  Your Private Key → Controls: " + signing_address)
print("  Your Proxy Wallet (where $49.97 is) → Different address!")
print()
print("You need to find your PROXY WALLET address.")
print()

print("=" * 70)
print("HOW TO FIND YOUR PROXY WALLET ADDRESS")
print("=" * 70)
print()
print("Option 1: Check Polymarket Website")
print("  1. Go to https://polymarket.com")
print("  2. Connect with your Magic Link account")
print("  3. Click your profile → Wallet/Account")
print("  4. Look for 'Deposit Address' or 'Wallet Address'")
print("  5. Copy that address - that's your FUNDER_ADDRESS")
print()
print("Option 2: Check Past Transactions")
print("  1. Go to https://polygonscan.com")
print("  2. Search your signing address: " + signing_address)
print("  3. Look at 'Internal Transactions' or 'Token Transfers'")
print("  4. Find the address you sent USDC to - that's the proxy")
print()
print("Option 3: Check Your Email")
print("  Magic Link may have sent you the wallet address when you signed up")
print()

print("=" * 70)
print("ONCE YOU FIND IT")
print("=" * 70)
print()
print("Update your .env file:")
print()
print("  SIGNATURE_TYPE=1")
print("  FUNDER_ADDRESS=0x_YOUR_PROXY_WALLET_ADDRESS")
print("  PRIVATE_KEY=0xe446cc68... (keep your Magic Link key)")
print()
print("The key insight:")
print("  - Private key signs the transactions")
print("  - Funder address holds the money (the proxy)")
print("  - They're DIFFERENT addresses for Magic Link wallets!")
print()

print("=" * 70)
print("IS THIS A BUILDER CODE WALLET?")
print("=" * 70)
print()
print("If you used a 'Builder Code' or referral code to sign up:")
print("  - You likely have a Magic Link wallet")
print("  - The proxy address should be in your Polymarket account")
print("  - Check your account settings on polymarket.com")
print()

print("Want me to help you verify once you find the proxy address?")
print("Just paste it here and I'll update the .env file for you.")
