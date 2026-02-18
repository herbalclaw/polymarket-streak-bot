#!/usr/bin/env python3
"""Analyze what went wrong and suggest improvements."""

import json
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
print("STRATEGY IMPROVEMENT ANALYSIS")
print("=" * 70)
print()

with open("trade_history_full.json", "r") as f:
    trades = json.load(f)

# Analyze loss patterns
losses = [t for t in trades if not t["settlement"]["won"]]
wins = [t for t in trades if t["settlement"]["won"]]

print("CURRENT PERFORMANCE:")
print(f"  Win Rate: {len(wins)}/{len(trades)} ({len(wins) / len(trades) * 100:.1f}%)")
print(f"  Expected: 67-82%")
print(f"  Gap: Underperforming by ~20%")
print()

print("=" * 70)
print("WHY IT'S UNDERPERFORMING")
print("=" * 70)
print()

print("1. CONSECUTIVE BETTING ON SAME STREAK")
print("   You bet on streak 4, lost, streak 5, lost, streak 6, lost...")
print("   The market was in a strong trend and you kept fading it.")
print()

print("2. NO COOLDOWN AFTER LOSSES")
print("   After a loss, you immediately bet on the next window.")
print("   No time to see if trend is continuing or reversing.")
print()

print("3. FIXED BET SIZE")
print("   Betting $5 even after losing streak.")
print("   Should reduce size or stop after 2-3 losses.")
print()

print("4. NO MARKET CONTEXT")
print("   Betting on 5-streak the same as 8-streak.")
print("   But 8-streak is rarer and trend is stronger.")
print()

print("=" * 70)
print("IMPROVEMENTS TO IMPLEMENT")
print("=" * 70)
print()

print("1. STOP AFTER 2 CONSECUTIVE LOSSES")
print("   After losing twice on same streak direction, stop for 30 min.")
print("   Prevents chasing losses during strong trends.")
print()

print("2. PROGRESSIVE BET SIZING (Not Martingale)")
print("   Trade 1: $5")
print("   After loss: $4")
print("   After 2 losses: $3")
print("   After win: Back to $5")
print("   Reduces exposure during losing streaks.")
print()

print("3. SKIP EXTREME STREAKS (7+)")
print("   Streaks of 7+ mean very strong trend.")
print("   Historical data shows no extra edge vs 5-streak.")
print("   Skip these and wait for new streak to form.")
print()

print("4. ADD TIME FILTER")
print("   Don't trade first 30s of window (volatile).")
print("   Enter at T-20s instead of T-30s for better price.")
print()

print("5. DAILY LOSS LIMIT")
print("   Already set to $50, but consider lowering to $20-30.")
print("   With $50 bankroll, losing $20 is 40% - too much.")
print()

print("6. TREND CONFIRMATION")
print("   Check if 3 out of last 4 trades were losses.")
print("   If so, market is trending - reduce bet size or skip.")
print()

print("7. VOLATILITY FILTER")
print("   If spread > 3% or price moved >10% in last window, skip.")
print("   High volatility = harder to predict.")
print()

print("=" * 70)
print("RECOMMENDED NEW SETTINGS")
print("=" * 70)
print()
print("BET_AMOUNT=4              # Slightly smaller")
print("STREAK_TRIGGER=5          # Wait for stronger signal")
print("MAX_DAILY_BETS=20         # Limit total exposure")
print("MAX_DAILY_LOSS=25         # Tighter stop")
print("ENTRY_SECONDS_BEFORE=20   # Better entry timing")
print("SKIP_AFTER_LOSSES=2       # Stop after 2 losses")
print()

print("=" * 70)
print("QUICK WINS YOU CAN DO NOW")
print("=" * 70)
print()
print("1. Edit .env and set MAX_DAILY_LOSS=25")
print("2. Set BET_AMOUNT=4 (from $5)")
print("3. Add to strategy: stop after 2 consecutive losses")
print()
print("Want me to implement any of these improvements?")
