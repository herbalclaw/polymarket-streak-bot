#!/usr/bin/env python3
"""Calculate max consecutive loss streak."""

import json

with open("trade_history_full.json", "r") as f:
    trades = json.load(f)

# Sort by timestamp to get chronological order
trades_sorted = sorted(trades, key=lambda x: x["execution"]["timestamp"])

# Calculate consecutive losses
current_loss_streak = 0
max_loss_streak = 0
loss_streaks = []

for trade in trades_sorted:
    if not trade["settlement"]["won"]:
        current_loss_streak += 1
        max_loss_streak = max(max_loss_streak, current_loss_streak)
    else:
        if current_loss_streak > 0:
            loss_streaks.append(current_loss_streak)
        current_loss_streak = 0

# Don't forget the last streak if it ended on a loss
if current_loss_streak > 0:
    loss_streaks.append(current_loss_streak)

print("=" * 70)
print("CONSECUTIVE LOSS ANALYSIS")
print("=" * 70)
print()
print(f"Current Loss Streak: {current_loss_streak}")
print(f"Maximum Loss Streak: {max_loss_streak}")
print()
if loss_streaks:
    print(f"All Loss Streaks: {loss_streaks}")
    print(f"Average Streak Length: {sum(loss_streaks) / len(loss_streaks):.1f}")
print()
print("=" * 70)

# Show the actual streak
if current_loss_streak > 0:
    print(f"\nYou are currently on a {current_loss_streak}-loss streak!")
    print("\nLast few trades:")
    for t in trades_sorted[-current_loss_streak - 2 :]:
        result = "LOSS" if not t["settlement"]["won"] else "WIN"
        print(
            f"  {t['position']['direction'].upper()} ${t['position']['amount']:.2f} -> {t['settlement']['outcome'].upper()} [{result}]"
        )
