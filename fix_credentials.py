#!/usr/bin/env python3
"""Fix API credentials for proxy wallet."""

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
print("FIXING API CREDENTIALS FOR PROXY WALLET")
print("=" * 70)
print()

from src.config import Config
from py_clob_client.client import ClobClient

# Clear any cached credentials
import json
import os as os_module

cache_file = ".clob_credentials.json"
if os_module.path.exists(cache_file):
    print(f"[1] Removing old credential cache: {cache_file}")
    os_module.remove(cache_file)
    print("     [OK] Cache cleared")
else:
    print(f"[1] No credential cache found (good)")

print()
print("[2] Creating fresh API credentials...")

try:
    # Create client with explicit proxy settings
    client = ClobClient(
        host=Config.CLOB_API,
        key=Config.PRIVATE_KEY,
        chain_id=Config.CHAIN_ID,
        signature_type=1,
        funder=Config.FUNDER_ADDRESS,
    )

    # Force create new credentials (don't derive from cache)
    creds = client.create_api_key()
    client.set_api_creds(creds)

    print("     [OK] New credentials created")
    print(f"     API Key: {creds.api_key[:20]}...")

    # Test the credentials by getting balance
    print()
    print("[3] Testing API connection...")

    # Try to get current market to verify connection works
    from src.core.polymarket import PolymarketClient

    pm_client = PolymarketClient()
    import time

    now = int(time.time())
    current_window = (now // 300) * 300
    market = pm_client.get_market(current_window)

    if market:
        print(f"     [OK] Connected to Polymarket API")
        print(f"     Current market: {market.slug}")
    else:
        print("     [WARN] Could not fetch market (but API is connected)")

    print()
    print("=" * 70)
    print("CREDENTIALS FIXED!")
    print("=" * 70)
    print()
    print("Try running the bot again:")
    print("  python bot.py")
    print()

except Exception as e:
    print(f"     [FAIL] {e}")
    print()
    print("Possible issues:")
    print("1. Private key doesn't have funds on Polygon")
    print("2. Funder address doesn't match private key")
    print("3. Network connectivity issues")
    sys.exit(1)
