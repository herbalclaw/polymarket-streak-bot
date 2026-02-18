#!/usr/bin/env python3
"""Quick test to verify balance detection before running live bot."""

import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, ".")

from src.core.trader import TradingState
from src.config import Config

# Load the trading state
state = TradingState.load()

print(f"[OK] Balance detected: ${state.bankroll:.2f}")
print(f"[OK] Config: MIN_BET=${Config.MIN_BET}, BET_AMOUNT=${Config.BET_AMOUNT}")
print(f"[OK] Can trade: {state.can_trade()}")
print(f"[OK] Daily bets: {state.daily_bets}")
print(f"[OK] Daily PnL: ${state.daily_pnl:+.2f}")

# Check if bankroll is exactly what we set
if abs(state.bankroll - 49.97) < 0.01:
    print("\n[SUCCESS] Balance of $49.97 is correctly detected!")
else:
    print(f"\n[WARNING] Expected $49.97 but found ${state.bankroll:.2f}")
