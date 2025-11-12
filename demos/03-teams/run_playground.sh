#!/bin/bash
# Quick script to test Teams bot with Agents Playground
# Uses the same Genie space as Slack: 01f0be3dcc771e60ada71b6ec9f61870

echo "============================================================"
echo "🤖 Teams Bot - Agents Playground Test"
echo "============================================================"
echo ""

# Check if Agents Playground is installed
if ! command -v agentsplayground &> /dev/null; then
    echo "❌ Agents Playground not found!"
    echo ""
    echo "Install it with:"
    echo "  npm install -g @microsoft/m365agentsplayground"
    echo ""
    exit 1
fi

echo "✅ Agents Playground found"
echo ""

# Check .env file
if [ ! -f "../../.env" ]; then
    echo "⚠️  .env file not found in project root"
    echo "   Make sure you have:"
    echo "   GENIE_SPACE_ID=01f0be3dcc771e60ada71b6ec9f61870"
    echo ""
fi

echo "Starting bot on port 3978..."
echo ""
echo "In another terminal, run:"
echo "  agentsplayground -e \"http://localhost:3978/api/messages\" -c \"emulator\""
echo ""
echo "============================================================"
echo ""

# Start the bot
python test_teams_bot.py

