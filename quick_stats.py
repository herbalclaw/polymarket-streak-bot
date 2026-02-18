#!/usr/bin/env python3
"""Quick trade stats summary."""

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
print("TRADING PERFORMANCE SUMMARY")
print("=" * 70)
print()

with open("trade_history_full.json", "r") as f:
    trades = json.load(f)

# Calculate stats
wins = [t for t in trades if t["settlement"]["won"]]
losses = [t for t in trades if not t["settlement"]["won"]]
total_pnl = sum(t["settlement"]["net_profit"] for t in trades)
total_fees = sum(t["settlement"]["fee_amount"] for t in trades)

print(f"Total Trades: {len(trades)}")
print(f"Wins: {len(wins)}")
print(f"Losses: {len(losses)}")
print(f"Win Rate: {len(wins) / len(trades) * 100:.1f}%" if trades else "N/A")
print()
print(f"Gross Profit: ${sum(t['settlement']['gross_profit'] for t in trades):+.2f}")
print(f"Total Fees: ${total_fees:.2f}")
print(f"Net PnL: ${total_pnl:+.2f}")
print()

if trades:
    last_trade = trades[-1]
    print("=" * 70)
    print("LATEST TRADE (JUST SETTLED)")
    print("=" * 70)
    print(f"Time: {last_trade['market']['slug']}")
    print(
        f"Bet: {last_trade['position']['direction'].upper()} ${last_trade['position']['amount']:.2f}"
    )
    print(f"Outcome: {last_trade['settlement']['outcome'].upper()}")

    if last_trade["settlement"]["won"]:
        print(f"Result: WIN +${last_trade['settlement']['net_profit']:.2f}")
    else:
        print(f"Result: LOSS -${abs(last_trade['settlement']['net_profit']):.2f}")

    print()
    print("Current streak without stop-loss protection is risky!")
    print("You've had some consecutive losses recently.")
    print()
    print("Recent trades (last 5):")
    for t in trades[-5:]:
        outcome = "WIN" if t["settlement"]["won"] else "LOSS"
        print(
            f"  {t['position']['direction'].upper()} ${t['position']['amount']:.2f} -> {t['settlement']['outcome'].upper()} [{outcome}]"
        )

print()
print("=" * 70)
print("STATUS")
print("=" * 70)
print(f"Current Bankroll: ~${49.97 + total_pnl:.2f}")
print(f"Daily Loss: ${total_pnl:+.2f}")
print(f"Max Daily Loss: $50")

if total_pnl <= -50:
    print("⚠️ DAILY LOSS LIMIT REACHED - Bot should stop trading!")
elif total_pnl <= -30:
    print("⚠️ Significant losses - Consider stopping for today")
else:
    print("✓ Within daily loss limits")
