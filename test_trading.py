#!/usr/bin/env python3
"""Test live trading API without placing actual order."""

import sys
import os

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.core.trader import LiveTrader, TradingState
from src.core.polymarket import PolymarketClient
from src.config import Config
import time

print("=" * 70)
print("LIVE TRADING API TEST")
print("=" * 70)
print()

# Test 1: Wallet credentials
print("[TEST 1] Wallet credentials...")
from web3 import Web3

w3 = Web3()
account = w3.eth.account.from_key(Config.PRIVATE_KEY)
if account.address.lower() == Config.FUNDER_ADDRESS.lower():
    print("  [PASS] Private key matches funder address")
else:
    print("  [FAIL] Address mismatch")
    sys.exit(1)

# Test 2: Initialize trader
print("[TEST 2] Initialize trader...")
try:
    trader = LiveTrader()
    print("  [PASS] Trader initialized successfully")
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

# Test 3: Get current market
print("[TEST 3] Get current market...")
client = PolymarketClient()
now = int(time.time())
current_window = (now // 300) * 300
market = client.get_market(current_window)
if market:
    print(f"  [PASS] Market: {market.slug}")
    print(f"         Up: {market.up_price:.3f}, Down: {market.down_price:.3f}")
    print(f"         Accepting orders: {market.accepting_orders}")
else:
    print("  [FAIL] Could not fetch market")
    sys.exit(1)

# Test 4: Check trading state
print("[TEST 4] Trading state...")
state = TradingState.load()
print(f"  [INFO] Balance: ${state.bankroll:.2f}")
print(f"  [INFO] Can trade: {state.can_trade()[0]}")

print()
print("=" * 70)
print("ALL TESTS PASSED")
print("=" * 70)
print()
print("The bot is ready to trade!")
print("Wallet: Configured correctly")
print("API: Connected")
print("Strategy: Streak reversal (bet AGAINST 4+ streaks)")
print()
print("Next step: Run 'python bot.py' and wait for a 4+ streak to form")
print("The bot will automatically place trades when conditions are met.")
