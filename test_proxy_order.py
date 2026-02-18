#!/usr/bin/env python3
"""Test place tiny order to initialize/fix proxy wallet credentials."""

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
print("TESTING PROXY WALLET ORDER (SMALL AMOUNT)")
print("=" * 70)
print()

from src.config import Config
from src.core.trader import LiveTrader
from src.core.polymarket import PolymarketClient
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
print(f"       Accepting orders: {market.accepting_orders}")
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

# Try to place a tiny test order
print("[3] Placing test order ($1)...")
print("   This will test if the proxy wallet can sign orders correctly.")
print()

try:
    # Determine direction based on price
    if market.up_price > market.down_price:
        direction = "down"  # Bet on the cheaper side
    else:
        direction = "up"

    print(f"   Direction: {direction.upper()}")
    print(f"   Amount: $1.00")
    print()

    trade = trader.place_bet(
        market=market,
        direction=direction,
        amount=1.0,  # $1 test
        confidence=0.5,
        streak_length=0,
    )

    if trade:
        print("=" * 70)
        print("SUCCESS! Order placed.")
        print("=" * 70)
        print(f"Order ID: {trade.timestamp}")
        print(f"Direction: {trade.direction.upper()}")
        print(f"Amount: ${trade.amount:.2f}")
        print()
        print("The wallet is now working correctly!")
        print("You can run the bot: python bot.py")
    else:
        print("=" * 70)
        print("ORDER REJECTED (but no error)")
        print("=" * 70)
        print("The order was rejected, possibly due to:")
        print("- Minimum order size ($5 on Polymarket)")
        print("- Market not accepting orders")
        print("- Insufficient funds")
        print()
        print("Let's try with $5...")
        print()

except Exception as e:
    print(f"  [ERROR] {e}")
    print()
    print("This is the signature error. Let's try a different approach...")
    print()

    # Try to reset and recreate
    print("[4] Attempting credential reset...")
    try:
        # Force reinitialization
        trader._init_client()
        print("  [OK] Client reinitialized")

        print("[5] Trying order again with fresh credentials...")
        direction = "up" if market.up_price <= market.down_price else "down"
        trade = trader.place_bet(
            market=market,
            direction=direction,
            amount=5.0,
            confidence=0.5,
            streak_length=0,
        )

        if trade:
            print("=" * 70)
            print("SUCCESS! Order placed after reset.")
            print("=" * 70)
        else:
            print("=" * 70)
            print(
                "Still failed. The proxy wallet may need to be set up on Polymarket first."
            )
            print("=" * 70)
            print()
            print("SOLUTION:")
            print("1. Go to https://polymarket.com")
            print("2. Connect your Magic Link wallet")
            print("3. Make a small deposit or place a manual trade first")
            print("4. This initializes the proxy wallet on-chain")
            print("5. Then run this script again")

    except Exception as e2:
        print(f"  [FAIL] {e2}")
        print()
        print("The proxy wallet needs to be initialized on Polymarket first.")
        print("Please make a manual trade or deposit on the website.")
