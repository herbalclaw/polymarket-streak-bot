#!/usr/bin/env python3
"""Test order placement with fixed EOA wallet."""

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
print("TESTING EOA WALLET ORDER")
print("=" * 70)
print()

from src.config import Config
from src.core.trader import LiveTrader
from src.core.polymarket import PolymarketClient
import time

print(
    f"Signature Type: {'Proxy/Magic (1)' if Config.SIGNATURE_TYPE == 1 else 'EOA/MetaMask (0)'}"
)
print(f"Paper Mode: {Config.PAPER_TRADE}")
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
print()

# Initialize trader
print("[2] Initializing trader...")
try:
    trader = LiveTrader()
    print("  [OK] Trader initialized")
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

print()

# Try to place a small test order
print("[3] Placing test order ($5)...")
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
        print(f"Price: {trade.execution_price:.3f}")
        print()
        print("The wallet is working correctly!")
        print("Run: python bot.py")
    else:
        print()
        print("=" * 70)
        print("ORDER NOT PLACED")
        print("=" * 70)
        print("This might be normal if the order was rejected.")

except Exception as e:
    print(f"  [ERROR] {e}")
    print()
    print("=" * 70)
    print("ERROR PLACING ORDER")
    print("=" * 70)
    print(f"Error: {e}")
