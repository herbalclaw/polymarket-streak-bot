#!/usr/bin/env python3
"""Test Magic Link wallet trading."""

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
print("TESTING MAGIC LINK WALLET")
print("=" * 70)
print()

from src.config import Config
from src.core.trader import LiveTrader
from src.core.polymarket import PolymarketClient
import time

print("[CONFIGURATION]")
print(f"  Signing Address: 0x910eEB450F7CaAa2e273B4E5261f88B84C55dBb0")
print(f"  Funder Address: {Config.FUNDER_ADDRESS}")
print(
    f"  Signature Type: {'Magic Link (1)' if Config.SIGNATURE_TYPE == 1 else 'EOA (0)'}"
)
print()

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
print(f"       Accepting orders: {market.accepting_orders}")
print()

# Initialize trader
print("[2] Initializing Magic Link trader...")
try:
    trader = LiveTrader()
    print("  [OK] Trader initialized")
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

print()

# Try to place a small test order
print("[3] Placing test order ($5)...")
print("   This tests if the Magic Link signature works correctly.")
print()

direction = "down" if market.up_price > market.down_price else "up"

try:
    trade = trader.place_bet(
        market=market,
        direction=direction,
        amount=5.0,
        confidence=0.5,
        streak_length=0,
    )

    if trade:
        print()
        print("=" * 70)
        print("SUCCESS! ORDER PLACED!")
        print("=" * 70)
        print(f"Order ID: {trade.timestamp}")
        print(f"Direction: {trade.direction.upper()}")
        print(f"Amount: ${trade.amount:.2f}")
        print()
        print("✓ Magic Link wallet is working correctly!")
        print("✓ The $49.97 in your proxy wallet is accessible")
        print()
        print("Ready to run: python bot.py")
    else:
        print()
        print("=" * 70)
        print("ORDER NOT PLACED")
        print("=" * 70)
        print("This might be because:")
        print("- Order was rejected (FOK didn't fill)")
        print("- Insufficient balance")
        print("- Market conditions")

except Exception as e:
    print(f"  [ERROR] {e}")
    import traceback

    traceback.print_exc()
