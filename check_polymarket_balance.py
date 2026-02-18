#!/usr/bin/env python3
"""Check Polymarket CTF exchange balance."""

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
print("CHECKING POLYMARKET EXCHANGE BALANCE")
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

# Get wallet address
account = w3.eth.account.from_key(Config.PRIVATE_KEY)
address = account.address

print(f"Wallet Address: {address}")
print()

# Polymarket CTF Exchange contract
ctf_exchange = "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"

# ERC20 balanceOf ABI
balance_abi = [
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
usdc_contract = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
usdc = w3.eth.contract(address=usdc_contract, abi=balance_abi)
usdc_balance = usdc.functions.balanceOf(address).call()
decimals = usdc.functions.decimals().call()
usdc_formatted = usdc_balance / (10**decimals)

print(f"USDC in Wallet: ${usdc_formatted:.2f}")

# Check if USDC is deposited to CTF Exchange
usdc_in_exchange = usdc.functions.balanceOf(ctf_exchange).call()
print(f"USDC in CTF Exchange Contract: ${usdc_in_exchange / (10**decimals):.2f}")

# Check collateral token balance (represents deposited USDC)
# Polymarket uses a conditional tokens framework
collateral_token = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"  # USDC

# Alternative: Check using Polymarket API
print()
print("[Checking via Polymarket CLOB API...]")
print()

try:
    from py_clob_client.client import ClobClient

    clob_client = ClobClient(
        host=Config.CLOB_API,
        key=Config.PRIVATE_KEY,
        chain_id=Config.CHAIN_ID,
        signature_type=0,
    )

    creds = clob_client.create_or_derive_api_creds()
    clob_client.set_api_creds(creds)

    # Try to get user data
    # The CLOB API might have a balance endpoint
    print("API credentials created successfully")

    # Check if we can get orders (indicates working connection)
    try:
        # Try to get the API to tell us balance info
        print()
        print("Checking via direct API call...")

        import requests

        headers = {
            "POLYMARKET_API_KEY": creds.api_key,
        }

        # Try to get balance endpoint
        resp = requests.get(f"{Config.CLOB_API}/balance", headers=headers, timeout=10)

        if resp.status_code == 200:
            print(f"Balance API response: {resp.json()}")
        else:
            print(f"Balance endpoint returned: {resp.status_code}")

    except Exception as e:
        print(f"Could not check balance via API: {e}")

except Exception as e:
    print(f"Error with CLOB client: {e}")

print()
print("=" * 70)
print("DIAGNOSIS")
print("=" * 70)
print()

if usdc_formatted >= 5:
    print(f"You have ${usdc_formatted:.2f} USDC in your wallet.")
    print()
    print("But you need to DEPOSIT it to Polymarket to trade.")
    print()
    print("TO DEPOSIT:")
    print("1. Go to https://polymarket.com")
    print("2. Connect wallet: 0x910eEB450F7CaAa2e273B4E5261f88B84C55dBb0")
    print("3. Click your profile → Deposit")
    print("4. Approve and deposit USDC")
    print()
    print("Once deposited, you can trade!")
else:
    print(f"Your wallet has ${usdc_formatted:.2f} USDC on Polygon.")
    print()
    print("If you believe you have $49.97, it might be:")
    print("1. On a different network (Ethereum instead of Polygon)")
    print("2. Already deposited to Polymarket but not showing in API")
    print("3. In a different wallet address")
    print()
    print("Check on Polygonscan:")
    print(f"https://polygonscan.com/address/{address}#tokentxns")
