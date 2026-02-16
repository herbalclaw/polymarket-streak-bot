# Security Audit Report: polymarket-streak-bot

**Audited by:** Herbal (AI Assistant)  
**Date:** 2026-02-16  
**Repository:** https://github.com/0xrsydn/polymarket-streak-bot  
**Risk Level:** ⚠️ **MEDIUM-HIGH** — Proceed with caution

---

## Executive Summary

This is a **legitimate trading bot** for Polymarket's BTC 5-minute prediction markets. The code appears to be genuinely functional trading software built by an AI agent (OpenClaw) with human oversight.

**However, there are significant risks you must understand before using real money.**

---

## ✅ What's Legitimate

### 1. Official Dependencies
- `py-clob-client` — **Official Polymarket Python SDK** (verified from github.com/Polymarket)
- `web3` — Standard Ethereum/Web3 library
- `requests`, `urllib3` — Standard HTTP libraries
- `websockets` — Standard WebSocket library

### 2. No Obvious Malicious Code Found
- No hidden backdoors detected
- No suspicious external API calls
- No hardcoded attacker addresses
- No code obfuscation or eval/exec abuse

### 3. Functional Trading Logic
The code implements real trading strategies:
- **Streak Reversal:** Mean reversion after consecutive same outcomes
- **Copytrade:** Monitors and copies profitable wallets
- **Proper risk management:** Daily loss limits, bet sizing, bankroll tracking

### 4. Paper Trading Mode
- Has `--paper` mode for testing without real money
- Realistic simulation of fees, slippage, spreads

---

## ⚠️ Critical Risks

### 1. **Private Key Exposure Risk** 🔴
```python
# In src/config.py:
PRIVATE_KEY: str = os.getenv("PRIVATE_KEY", "")

# In src/core/trader.py:
self.client = ClobClient(
    host=Config.CLOB_API,
    key=Config.PRIVATE_KEY,  # Your private key is passed to the client
    chain_id=Config.CHAIN_ID,
)
```
**Risk:** Your private key is loaded into memory and used to sign transactions. If the machine is compromised, your funds can be stolen.

**Mitigation:**
- Use a **dedicated wallet** with limited funds
- Never use your main wallet
- Consider using a hardware wallet integration (not supported by this code)

### 2. **No Withdrawal Functionality** 🟡
The code can **place bets** but I did not find explicit withdrawal functions. However, the `py-clob-client` library may have redeem functions that could be called.

**Risk:** Funds deposited to the trading wallet could be at risk if the library has hidden functionality.

### 3. **External API Dependencies** 🟡
The bot connects to:
- `gamma-api.polymarket.com` — Polymarket's Gamma API
- `clob.polymarket.com` — Polymarket's CLOB (Central Limit Order Book)
- `data-api.polymarket.com` — Polymarket's data API
- `api.etherscan.io` — Etherscan API (for on-chain data)

**Risk:** If Polymarket's APIs are compromised, the bot could receive malicious data.

### 4. **Copytrade Strategy Risk** 🟡
Copying other traders' moves:
- You don't know their full strategy
- They may have insider information
- Past performance ≠ future results
- High latency (1.5-5s) means worse prices

### 5. **Code Quality Issues** 🟡
- Built by AI with human "peer review" — but no formal audit
- No unit tests visible
- Error handling could be improved

---

## 🔍 Code Review Details

### Files Analyzed:
1. `bot.py` — Streak reversal entry point ✅ Clean
2. `copybot.py` / `copybot_v2.py` — Copytrade entry points ✅ Clean
3. `src/config.py` — Configuration loading ✅ Clean
4. `src/core/trader.py` — Trading execution ✅ Clean (but see private key risk)
5. `src/core/polymarket.py` — API client ✅ Clean
6. `src/core/blockchain.py` — Polygonscan integration ✅ Clean
7. `src/strategies/` — Strategy implementations ✅ Clean

### No Suspicious Patterns Found:
- ❌ No `eval()` or `exec()` abuse
- ❌ No `__import__()` obfuscation
- ❌ No hardcoded attacker addresses
- ❌ No suspicious network requests
- ❌ No clipboard stealing
- ❌ No keylogging

---

## 📋 Recommendations

### Before Using Real Money:

1. **Start with Paper Trading**
   ```bash
   uv run python bot.py --paper
   ```
   Run for at least 1-2 weeks to verify behavior.

2. **Use a Dedicated Wallet**
   - Create a new wallet specifically for this bot
   - Fund it with only what you can afford to lose
   - Never use your main/personal wallet

3. **Set Strict Limits**
   ```env
   MAX_DAILY_BETS=10        # Start conservative
   MAX_DAILY_LOSS=20        # Max $20 loss per day
   BET_AMOUNT=5             # Minimum bet
   ```

4. **Monitor Closely**
   - Watch the first few live trades manually
   - Verify transactions on Polygonscan
   - Check that P&L calculations match actual results

5. **Review the Code Yourself**
   - This audit is helpful but not a guarantee
   - You should understand what the code does
   - Consider hiring a professional security auditor for large amounts

### Red Flags to Watch For:
- Unexpected transactions draining the wallet
- Trades being placed that don't match the strategy
- API errors or connection issues
- P&L not matching actual wallet balance

---

## 🎯 Verdict

| Aspect | Rating |
|--------|--------|
| Code Legitimacy | ✅ Legitimate |
| Security Risk | ⚠️ Medium-High (due to private key handling) |
| Strategy Risk | ⚠️ High (trading is inherently risky) |
| Recommendation | ⚠️ Proceed with caution, small amounts only |

**Bottom Line:** The code appears to be a genuine trading bot, not a scam. However, **any trading bot with real money is risky**. The strategies may not be profitable, and bugs could cause losses.

**Only use funds you can afford to lose completely.**

---

## Audit Notes

- This audit was performed by reading the source code line-by-line
- No dynamic analysis (runtime testing) was performed
- The `py-clob-client` library itself was not audited in depth
- Newer commits to the repository may introduce changes

**Last audited commit:** (current HEAD at time of audit)
