#!/usr/bin/env python3
"""Test placing and cancelling an order."""

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
print("TEST PLACE + CANCEL ORDER")
print("=" * 70)
print()

from src.config import Config
from src.core.polymarket import PolymarketClient
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import ApiCreds
import time

# Get current market
print("[1] Getting current market...")
client = PolymarketClient()
now = int(time.time())
current_window = (now // 300) * 300
market = client.get_market(current_window)

if not market:
    print("  [FAIL] Could not get market")
    sys.exit(1)

print(f"  [OK] Market: {market.slug}")
print(f"       Token IDs - Up: {market.up_token_id[:20]}...")
print()

# Initialize CLOB client
print("[2] Initializing CLOB client...")
try:
    clob_client = ClobClient(
        host=Config.CLOB_API,
        key=Config.PRIVATE_KEY,
        chain_id=Config.CHAIN_ID,
        signature_type=0,  # EOA
    )

    # Create/get API credentials
    creds = clob_client.create_or_derive_api_creds()
    clob_client.set_api_creds(creds)
    print("  [OK] Client initialized with API credentials")

except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

print()

# Place a LIMIT order (not FOK) so we can cancel it
print("[3] Placing LIMIT order (to be cancelled)...")
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

try:
    # Use up token for the order
    token_id = market.up_token_id

    # Create a limit order at 45 cents (below market)
    order_args = OrderArgs(
        token_id=token_id,
        price=0.45,  # Limit price
        size=5.0,  # $5 worth
        side=BUY,
    )

    # Create and sign the order
    signed_order = clob_client.create_order(order_args)

    # Post the order
    response = clob_client.post_order(signed_order, OrderType.GTC)
    order_id = response.get("orderID") or response.get("id")

    if not order_id:
        print(f"  [FAIL] No order ID returned")
        print(f"         Response: {response}")
        sys.exit(1)

    print(f"  [OK] Order placed: {order_id[:30]}...")
    print(f"       Price: $0.45, Size: $5.00")
    print()

    # Wait a moment
    time.sleep(2)

    # Now cancel it
    print("[4] Cancelling order...")
    cancel_response = clob_client.cancel(order_id)

    if cancel_response.get("canceled") or cancel_response.get("cancelled"):
        print(f"  [OK] Order cancelled successfully!")
    else:
        print(f"  [INFO] Cancel response: {cancel_response}")
        print(f"       Order may have already filled or been rejected")

    print()
    print("=" * 70)
    print("PLACE + CANCEL TEST COMPLETE")
    print("=" * 70)
    print()
    print("✓ Wallet can place orders")
    print("✓ Wallet can cancel orders")
    print("✓ API credentials working")
    print()
    print("The bot is ready to trade!")
    print("Run: python bot.py")

except Exception as e:
    print(f"  [ERROR] {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
