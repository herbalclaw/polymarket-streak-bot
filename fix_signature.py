#!/usr/bin/env python3
"""Fix proxy wallet signature issue by switching modes or reconfiguring."""

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
print("FIXING PROXY WALLET SIGNATURE ERROR")
print("=" * 70)
print()

from src.config import Config
from web3 import Web3

# First, let's understand the wallet setup
print("[DIAGNOSIS]")
print(
    f"Current Signature Type: {'Proxy/Magic (1)' if Config.SIGNATURE_TYPE == 1 else 'EOA/MetaMask (0)'}"
)
print(f"Funder Address: {Config.FUNDER_ADDRESS}")

# Check what address the private key actually controls
w3 = Web3()
account = w3.eth.account.from_key(Config.PRIVATE_KEY)
derived_address = account.address
print(f"Private Key Controls: {derived_address}")
print()

if derived_address.lower() == Config.FUNDER_ADDRESS.lower():
    print("[OK] Private key matches funder address")
    print()

    # The issue is likely that this is actually an EOA wallet, not a proxy
    print("[ANALYSIS]")
    print("Your private key derives to the same address as the funder.")
    print("This means you have an EOA (standard) wallet, not a proxy wallet.")
    print()
    print("[FIX NEEDED]")
    print("Change SIGNATURE_TYPE from 1 to 0 in your .env file")
    print()

    # Auto-fix
    env_path = ".env"
    with open(env_path, "r") as f:
        content = f.read()

    if "SIGNATURE_TYPE=1" in content:
        print("Applying fix now...")
        content = content.replace("SIGNATURE_TYPE=1", "SIGNATURE_TYPE=0")
        # Also remove or comment out FUNDER_ADDRESS since it's not needed for EOA
        content = content.replace(
            f"FUNDER_ADDRESS={Config.FUNDER_ADDRESS}",
            f"# FUNDER_ADDRESS={Config.FUNDER_ADDRESS}  # Not needed for EOA wallets",
        )

        with open(env_path, "w") as f:
            f.write(content)

        print("[DONE] Fixed! SIGNATURE_TYPE changed to 0 (EOA mode)")
        print()
        print("Next steps:")
        print("1. Run: python bot.py")
        print("2. The bot should now place trades successfully")
    else:
        print("SIGNATURE_TYPE is already set correctly")

else:
    print("[ERROR] Address mismatch!")
    print(f"Private key derives to: {derived_address}")
    print(f"But FUNDER_ADDRESS is: {Config.FUNDER_ADDRESS}")
    print()
    print("You need to:")
    print("1. Get the correct private key for your funder address")
    print("2. Or update FUNDER_ADDRESS to match your private key")
    print()
    print(f"Suggested fix: Set FUNDER_ADDRESS={derived_address}")
