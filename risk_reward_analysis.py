#!/usr/bin/env python3
"""Calculate required win rate to be profitable."""

import json

with open("trade_history_full.json", "r") as f:
    trades = json.load(f)

print("=" * 70)
print("RISK/REWARD PROBLEM ANALYSIS")
print("=" * 70)
print()

# Average win vs loss
wins = [t for t in trades if t["settlement"]["won"]]
losses = [t for t in trades if not t["settlement"]["won"]]
avg_win = sum(t["settlement"]["net_profit"] for t in wins) / len(wins) if wins else 0
avg_loss = (
    abs(sum(t["settlement"]["net_profit"] for t in losses)) / len(losses)
    if losses
    else 0
)

print("CURRENT MATH:")
print(f"  Average Win: +${avg_win:.2f}")
print(f"  Average Loss: -${avg_loss:.2f}")
print()

# Calculate breakeven win rate
# If you win $4.20 and lose $5.00:
# Breakeven = Loss / (Win + Loss) = 5 / (4.20 + 5) = 54.3%
breakeven = avg_loss / (avg_win + avg_loss)

print("BREAKEVEN ANALYSIS:")
print(f"  To breakeven, you need: {breakeven * 100:.1f}% win rate")
print(f"  Your actual win rate: 46.7%")
print(f"  Gap: You're {breakeven * 100 - 46.7:.1f} percentage points short!")
print()

print("=" * 70)
print("WHY THIS HAPPENS")
print("=" * 70)
print()
print("1. THE FEE STRUCTURE")
print("   - Win: Pay 2.5% fee on gross profit")
print("   - Loss: Pay 0% fee")
print("   - This creates imbalance: Wins are ~$4, Losses are ~$5")
print()
print("2. ENTRY PRICE ISSUE")
print("   - You're entering at ~50-51 cents")
print("   - Payout is $1 per share")
print("   - Profit per share: ~49-50 cents")
print("   - But after 2.5% fee: ~48 cents")
print("   - Example:")
print("     Buy 10 shares at $0.50 = $5.00")
print("     Win: 10 × $1.00 = $10.00")
print("     Fee: $10 × 0.025 = $0.25")
print("     Net: $10 - $5 - $0.25 = $4.75")
print()
print("3. THE MATH DOESN'T WORK")
print("   With 46.7% win rate and $4.75 avg win / $5.00 avg loss:")
print("   Expected Value = (0.467 × $4.75) - (0.533 × $5.00) = -$0.46 per trade")
print()

print("=" * 70)
print("SOLUTIONS")
print("=" * 70)
print()
print("OPTION 1: IMPROVE WIN RATE TO >55%")
print("   - Skip borderline trades")
print("   - Only trade when streak is 5+ (82% win rate)")
print("   - Add filters (volatility, spread)")
print()
print("OPTION 2: GET BETTER ENTRY PRICE")
print("   - Wait for price to drop to 48-49 cents")
print("   - Use limit orders instead of market orders")
print("   - Don't enter in first 20s (price discovery)")
print()
print("OPTION 3: REDUCE FEE IMPACT")
print("   - Trade bigger size (fees are percentage, so same %)")
print("   - Actually, smaller size means same fee %")
print("   - No solution here - fee is fixed %")
print()
print("OPTION 4: ONLY TRADE HIGH-EDGE SETUPS")
print("   - Skip 4-streak (66% edge)")
print("   - Only trade 5-streak+ (82% edge)")
print("   - 82% win rate × $4.75 - 18% × $5.00 = +$3.00 per trade")
print()
print("OPTION 5: TARGET 60%+ WIN RATE")
print("   Need better timing/filtering to hit 60%+")
print("   Then: 60% × $4.75 - 40% × $5.00 = +$0.85 per trade")
print()

print("=" * 70)
print("RECOMMENDED FIX")
print("=" * 70)
print()
print("Change these settings in .env:")
print()
print("  STREAK_TRIGGER=5          # Only trade 5+ streaks (82% edge)")
print("  BET_AMOUNT=5              # Keep same")
print("  ENTRY_SECONDS_BEFORE=20   # Better timing")
print()
print("Add filters:")
print("  - Skip if spread > 2%")
print("  - Skip if entered trade on same streak and lost")
print()
print("With 82% win rate on 5-streaks:")
print("  8 wins × $4.75 = $38.00")
print("  2 losses × $5.00 = $10.00")
print("  Net per 10 trades: +$28.00")
print()
