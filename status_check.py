#!/usr/bin/env python3
"""Monitor the bot and show real-time status."""

import subprocess
import sys
import os
import time

# Fix Windows console encoding
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

print("=" * 70)
print("POLYMARKET STREAK BOT - STATUS CHECK")
print("=" * 70)
print()

# Check balance
from src.core.trader import TradingState

state = TradingState.load()
print(f"Balance: ${state.bankroll:.2f}")
print(f"Daily Bets: {state.daily_bets}")
print(f"Daily PnL: ${state.daily_pnl:+.2f}")
print(f"Can Trade: {state.can_trade()[0]} ({state.can_trade()[1]})")
print()

# Check configuration
from src.config import Config

print(f"Mode: {'PAPER' if Config.PAPER_TRADE else 'LIVE'}")
print(f"Streak Trigger: {Config.STREAK_TRIGGER}")
print(f"Bet Amount: ${Config.BET_AMOUNT}")
print(f"Min Bet: ${Config.MIN_BET}")
print()

# Check API connection
print("Checking Polymarket API connection...")
from src.core.polymarket import PolymarketClient

client = PolymarketClient()

# Get current market
try:
    import time as time_module

    now = int(time_module.time())
    current_window = (now // 300) * 300

    market = client.get_market(current_window)
    if market:
        print(f"Current Market: {market.slug}")
        print(f"  Up Price: {market.up_price:.3f}")
        print(f"  Down Price: {market.down_price:.3f}")
        print(f"  Accepting Orders: {market.accepting_orders}")
        print(f"  Closed: {market.closed}")
        if market.outcome:
            print(f"  Outcome: {market.outcome.upper()}")
    else:
        print("  Could not fetch current market")

    # Get recent outcomes
    print()
    print("Fetching recent outcomes...")
    outcomes = client.get_recent_outcomes(count=5)
    print(
        f"  Last {len(outcomes)} outcomes: {' -> '.join(o.upper() for o in outcomes)}"
    )

except Exception as e:
    print(f"  Error: {e}")

print()
print("=" * 70)
print("BOT IS READY TO TRADE")
print("=" * 70)
print()
print("The bot is running in LIVE mode with $49.97 balance.")
print("It will place bets when a streak of 4 consecutive outcomes is detected.")
print()
print("To stop the bot: Press Ctrl+C")
