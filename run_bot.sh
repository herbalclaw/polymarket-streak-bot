#!/bin/bash
# Setup and run Polymarket streak bot locally
# Run this on YOUR machine, not shared

echo "=== Polymarket Streak Bot Setup ==="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "# Add your private key here" > .env
    echo "PRIVATE_KEY=0x_your_private_key_here" >> .env
    echo "PAPER_TRADE=false" >> .env
    echo "BET_AMOUNT=5" >> .env
    echo "MAX_DAILY_BETS=50" >> .env
    echo "MAX_DAILY_LOSS=50" >> .env
    echo "STREAK_TRIGGER=4" >> .env
    echo ""
    echo "⚠️  EDIT .env FILE AND ADD YOUR PRIVATE KEY BEFORE RUNNING"
    echo ""
    exit 1
fi

# Check if private key is set
if grep -q "0x_your_private_key_here" .env; then
    echo "❌ ERROR: You need to edit .env and add your actual private key"
    echo "   Replace '0x_your_private_key_here' with your real key"
    exit 1
fi

echo "✅ .env file configured"
echo ""

# Activate virtual environment
source venv/bin/activate

echo "Starting streak bot..."
echo "Mode: LIVE (real money)"
echo ""

# Run the bot
python bot.py --live
