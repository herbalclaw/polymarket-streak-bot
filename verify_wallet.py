#!/usr/bin/env python3
"""Verify wallet address from private key."""

import sys
import os

# Fix encoding
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.config import Config
from web3 import Web3


def verify_wallet():
    if not Config.PRIVATE_KEY:
        print("Error: PRIVATE_KEY not set in .env")
        return

    # Clean up private key
    private_key = Config.PRIVATE_KEY
    if private_key.startswith("0x"):
        private_key = private_key[2:]

    try:
        # Create Web3 account from private key
        w3 = Web3()
        account = w3.eth.account.from_key(private_key)
        derived_address = account.address

        print("=" * 60)
        print("WALLET VERIFICATION")
        print("=" * 60)
        print()
        print(f"Private Key:    {Config.PRIVATE_KEY[:10]}...{Config.PRIVATE_KEY[-6:]}")
        print(f"Derived Address: {derived_address}")
        print()
        print(f"Funder Address: {Config.FUNDER_ADDRESS}")
        print()

        if derived_address.lower() == Config.FUNDER_ADDRESS.lower():
            print("[OK] Private key matches funder address!")
        else:
            print("[MISMATCH] Private key does NOT match funder address!")
            print()
            print("Solutions:")
            print("1. Update FUNDER_ADDRESS to:", derived_address)
            print("2. Or use the correct private key for your funder address")

        print()
        print(
            "Signature Type:",
            "Proxy/Magic (1)" if Config.SIGNATURE_TYPE == 1 else "EOA/MetaMask (0)",
        )

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    verify_wallet()
