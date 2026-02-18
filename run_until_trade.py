#!/usr/bin/env python3
"""Run bot continuously until a trade is placed."""

import sys
import os
import time
import signal

# Fix Windows console encoding
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from datetime import datetime
from src.config import Config, LOCAL_TZ, TIMEZONE_NAME
from src.core.polymarket import PolymarketClient
from src.strategies.streak import evaluate
from src.core.trader import LiveTrader, TradingState

running = True


def handle_signal(sig, _frame):
    global running
    print("\n[bot] Shutting down...")
    running = False


signal.signal(signal.SIGINT, handle_signal)


def log(msg: str):
    ts = datetime.now(LOCAL_TZ).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


# Initialize
client = PolymarketClient()
state = TradingState.load()
trader = LiveTrader()

log("=" * 70)
log("LIVE STREAK BOT - WAITING FOR STREAK")
log("=" * 70)
log(f"Balance: ${state.bankroll:.2f}")
log(f"Strategy: Bet AGAINST {Config.STREAK_TRIGGER}+ streaks")
log(f"Mode: LIVE (real money)")
log("")
log("Waiting for a streak of 4+ consecutive outcomes...")
log("Press Ctrl+C to stop")
log("")

bet_timestamps = {t.timestamp for t in state.trades}
pending = []
traded = False
check_count = 0

while running and not traded:
    try:
        now = int(time.time())
        current_window = (now // 300) * 300
        seconds_into_window = now - current_window
        next_window = current_window + 300

        # Check for settled trades
        for trade in list(pending):
            market = client.get_market(trade.timestamp)
            if market and market.closed and market.outcome:
                state.settle_trade(trade, market.outcome)
                log(
                    f"[SETTLED] {trade.direction.upper()} -> {market.outcome.upper()} | PnL: ${trade.pnl:+.2f}"
                )
                pending.remove(trade)
                state.save()

        # Check if we can trade
        can_trade, reason = state.can_trade()
        if not can_trade:
            if check_count % 6 == 0:  # Log every minute
                log(f"[BLOCKED] {reason}")
            time.sleep(10)
            check_count += 1
            continue

        target_ts = next_window
        seconds_until_target = target_ts - now

        if target_ts in bet_timestamps:
            time.sleep(5)
            check_count += 1
            continue

        # Entry timing - enter 30 seconds before window opens
        if seconds_until_target > Config.ENTRY_SECONDS_BEFORE:
            if check_count % 6 == 0:  # Log every minute
                log(f"[WAIT] Next window in {seconds_until_target}s")
            time.sleep(10)
            check_count += 1
            continue

        # Time to evaluate
        log("[ANALYZE] Checking for streak...")
        outcomes = client.get_recent_outcomes(count=Config.STREAK_TRIGGER + 2)
        log(f"[DATA] Outcomes: {' -> '.join(o.upper() for o in outcomes)}")

        sig = evaluate(outcomes, trigger=Config.STREAK_TRIGGER)

        if not sig.should_bet:
            log(f"[NO BET] {sig.reason}")
            bet_timestamps.add(target_ts)
            time.sleep(10)
            check_count += 1
            continue

        # We have a signal!
        log(f"[SIGNAL] {sig.reason}")

        # Get market
        market = client.get_market(target_ts)
        if not market:
            log(f"[ERROR] Market not found")
            time.sleep(5)
            check_count += 1
            continue

        if not market.accepting_orders:
            log(f"[ERROR] Market not accepting orders")
            bet_timestamps.add(target_ts)
            time.sleep(5)
            check_count += 1
            continue

        entry_price = market.up_price if sig.direction == "up" else market.down_price
        log(f"[PRICE] {sig.direction.upper()} @ {entry_price:.3f}")

        # Place the trade
        log(f"[EXECUTE] Placing ${Config.BET_AMOUNT} on {sig.direction.upper()}...")
        trade = trader.place_bet(
            market=market,
            direction=sig.direction,
            amount=Config.BET_AMOUNT,
            confidence=sig.confidence,
            streak_length=sig.streak_length,
        )

        if trade is None:
            log("[FAILED] Order rejected")
            bet_timestamps.add(target_ts)
            check_count += 1
            continue

        # Success!
        state.record_trade(trade)
        bet_timestamps.add(target_ts)
        pending.append(trade)
        state.save()

        log("")
        log("=" * 70)
        log("TRADE PLACED SUCCESSFULLY!")
        log("=" * 70)
        log(f"Direction: {trade.direction.upper()}")
        log(f"Amount: ${trade.amount:.2f}")
        log(f"Price: {trade.execution_price:.3f}")
        log(f"Market: {trade.market_slug}")
        log("")
        log(f"Balance: ${state.bankroll:.2f}")
        log(f"Pending: {len(pending)} trade(s)")
        log("=" * 70)

        traded = True

    except KeyboardInterrupt:
        break
    except Exception as e:
        log(f"[ERROR] {e}")
        time.sleep(10)
        check_count += 1

# Save final state
state.save()

log("")
log("=" * 70)
log("SESSION COMPLETE")
log(f"Final Balance: ${state.bankroll:.2f}")
log(f"Daily Bets: {state.daily_bets}")
log(f"Daily PnL: ${state.daily_pnl:+.2f}")
log("=" * 70)
