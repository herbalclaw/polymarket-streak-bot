#!/usr/bin/env python3
"""Run bot with detailed logging."""

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
log("LIVE STREAK BOT STARTED")
log("=" * 70)
log(f"Balance: ${state.bankroll:.2f}")
log(f"Strategy: Bet AGAINST {Config.STREAK_TRIGGER}+ streaks")
log(f"Mode: LIVE (real money)")
log("")

bet_timestamps = {t.timestamp for t in state.trades}
pending = []

# Run for max 60 seconds or until trade is placed
start_time = time.time()
trade_placed = False

while running and (time.time() - start_time) < 60 and not trade_placed:
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
            log(f"[BLOCKED] {reason}")
            time.sleep(5)
            continue

        target_ts = next_window
        seconds_until_target = target_ts - now

        if target_ts in bet_timestamps:
            log(f"[SKIP] Already bet on window {target_ts}")
            time.sleep(5)
            continue

        # Entry timing
        if seconds_until_target > Config.ENTRY_SECONDS_BEFORE:
            if seconds_into_window % 30 == 0:
                log(
                    f"[WAIT] Next window in {seconds_until_target}s (enter at T-{Config.ENTRY_SECONDS_BEFORE}s)"
                )
            time.sleep(1)
            continue

        # Get outcomes and evaluate
        log("[ANALYZE] Fetching recent outcomes...")
        outcomes = client.get_recent_outcomes(count=Config.STREAK_TRIGGER + 2)
        log(f"[DATA] Recent: {' -> '.join(o.upper() for o in outcomes)}")

        sig = evaluate(outcomes, trigger=Config.STREAK_TRIGGER)

        if not sig.should_bet:
            log(f"[NO SIGNAL] {sig.reason}")
            bet_timestamps.add(target_ts)
            time.sleep(5)
            continue

        # Get market
        market = client.get_market(target_ts)
        if not market:
            log(f"[ERROR] Market not found for ts={target_ts}")
            time.sleep(5)
            continue

        if not market.accepting_orders:
            log(f"[ERROR] Market not accepting orders")
            bet_timestamps.add(target_ts)
            time.sleep(5)
            continue

        # Calculate bet
        entry_price = market.up_price if sig.direction == "up" else market.down_price
        log(f"[SIGNAL] {sig.reason}")
        log(f"[PRICE] {sig.direction.upper()} @ {entry_price:.3f}")

        # Execute trade
        log(f"[EXECUTE] Placing ${Config.BET_AMOUNT} bet on {sig.direction.upper()}...")
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
            continue

        state.record_trade(trade)
        bet_timestamps.add(target_ts)
        pending.append(trade)
        state.save()

        log(f"[SUCCESS] Trade placed! ID: {trade.timestamp}")
        log(f"[STATUS] Balance: ${state.bankroll:.2f} | Pending: {len(pending)}")
        trade_placed = True

        time.sleep(5)

    except KeyboardInterrupt:
        break
    except Exception as e:
        log(f"[ERROR] {e}")
        time.sleep(10)

state.save()
log("")
log("=" * 70)
log(f"SESSION COMPLETE")
log(f"Final Balance: ${state.bankroll:.2f}")
log(f"Daily Bets: {state.daily_bets}")
log(f"Daily PnL: ${state.daily_pnl:+.2f}")
log("=" * 70)
