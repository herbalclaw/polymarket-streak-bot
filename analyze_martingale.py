#!/usr/bin/env python3
"""Analyze Martingale strategy feasibility."""

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
print("MARTINGALE STRATEGY ANALYSIS")
print("=" * 70)
print()

# Current settings
bankroll = 49.97
min_bet = 2
streak_trigger = 4

print("[CURRENT SETUP]")
print(f"  Bankroll: ${bankroll}")
print(f"  Min Bet: ${min_bet}")
print(f"  Streak Trigger: {streak_trigger}")
print()

# Martingale progression after losses
print("[MARTINGALE PROGRESSION]")
print("After each loss, double the bet:")
print()

bet_sequence = []
current_bet = min_bet
total_risked = 0

for i in range(1, 7):
    total_risked += current_bet
    remaining = bankroll - total_risked
    status = (
        "✓" if current_bet <= bankroll and total_risked <= bankroll else "✗ BANKRUPT"
    )

    print(
        f"  Trade {i}: ${current_bet} (Total risked: ${total_risked}, Remaining: ${remaining:.2f}) {status}"
    )

    if total_risked > bankroll:
        print(f"\n  ❌ Cannot place trade {i} - insufficient funds!")
        break

    bet_sequence.append(current_bet)
    current_bet *= 2

print()
print("=" * 70)
print("PROBLEM: You can only survive 4 losses")
print("=" * 70)
print()
print("With $49.97 and min bet $2:")
print("  Loss 1: -$2 (bet $2, streak continues)")
print("  Loss 2: -$4 (bet $4, streak continues)")
print("  Loss 3: -$8 (bet $8, streak continues)")
print("  Loss 4: -$16 (bet $16, streak continues)")
print("  Loss 5: Need $32, but only have $19.97 left → CANNOT BET")
print()
print("After just 4 consecutive losses on a streak, you're out of money!")
print()

print("=" * 70)
print("WHY IT'S DANGEROUS")
print("=" * 70)
print()
print("The streak strategy already bets on reversals:")
print("  - 4 streak → 66.7% reversal rate")
print("  - 5 streak → 82.4% reversal rate")
print("  - 6+ streak → Still 82.4% (capped)")
print()
print("But if the streak continues:")
print("  - Trade 1: Bet $2 on streak 4 reversal → LOSE")
print("  - Trade 2: Bet $4 on streak 5 reversal → LOSE")
print("  - Trade 3: Bet $8 on streak 6 reversal → LOSE")
print("  - Trade 4: Bet $16 on streak 7 reversal → LOSE")
print("  - Trade 5: CANNOT BET, streak is now 8")
print()
print("You've lost $30 and can't place the 5th trade!")
print("If the 5th trade would have won, you miss it entirely.")
print()

print("=" * 70)
print("REALISTIC SCENARIO")
print("=" * 70)
print()
print("What if you get a 10-streak? (Happens sometimes!)")
print()
print("Your bets: $2 → $4 → $8 → $16 → [BANKRUPT]")
print("Streak continues to 9 or 10...")
print()
print("You lose $30 and miss the final winning trade.")
print("Then what? You can't recover.")
print()

print("=" * 70)
print("ALTERNATIVE: MODIFIED MARTINGALE")
print("=" * 70)
print()
print("Instead of doubling, use smaller increases:")
print("  Trade 1: $2")
print("  Trade 2: $3 (+50%)")
print("  Trade 3: $5 (+67%)")
print("  Trade 4: $8 (+60%)")
print("  Trade 5: $12 (+50%)")
print("  Total risked: $30 (survivable!)")
print()
print("Or: Stop after 2 consecutive losses and wait for new streak.")
print()

print("=" * 70)
print("RECOMMENDATION")
print("=" * 70)
print()
print("❌ DON'T use Martingale with only $49.97")
print("   - Too risky, can go bankrupt on 5th trade")
print("   - Streaks of 7-10 DO happen in crypto")
print()
print("✅ BETTER approach:")
print("   1. Keep flat betting ($5 per trade)")
print("   2. Trust the 67-82% edge")
print("   3. Use daily loss limit ($50) as protection")
print("   4. Build bankroll to $200+ before considering Martingale")
print()
print("Or if you want to try Martingale:")
print("   - Start with $1 (can survive 5-6 losses)")
print("   - Have at least $100-200 bankroll")
print("   - Set a max of 3-4 Martingale levels")
print()

print("Want me to implement a modified version with stop-loss?")
