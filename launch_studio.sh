#!/bin/bash

# LangGraph Studio Launcher
# Quick script to start LangGraph Studio with tunnel and open in browser

echo "🚀 Starting LangGraph Studio..."

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected. Activating..."
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ No virtual environment found at .venv/"
        echo "   Please run: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi
fi

# Kill any existing LangGraph processes
echo "🧹 Cleaning up existing processes..."
pkill -f langgraph 2>/dev/null || true
sleep 2

# Start LangGraph Studio locally (faster and more reliable for Chrome)
echo "🌐 Starting LangGraph Studio..."
langgraph dev &

# Wait for local server to start
echo "⏳ Waiting for server to start..."
sleep 4

# Check for local server availability
LOCAL_URL="http://localhost:2024"
echo "🔍 Checking local server..."
for i in {1..8}; do
    if curl -s --max-time 2 "$LOCAL_URL/openapi.json" > /dev/null 2>&1; then
        echo "✅ Local server is ready at $LOCAL_URL"
        STUDIO_URL="https://smith.langchain.com/studio/?baseUrl=$LOCAL_URL"
        break
    fi
    echo "   Attempt $i/8: Waiting for server..."
    sleep 2
done

if [ -z "$STUDIO_URL" ]; then
    echo "❌ Server failed to start. Check error messages above."
    exit 1
fi

echo ""
echo "🎨 LangGraph Studio is ready!"
echo "   Studio UI: $STUDIO_URL"
echo "   API Docs:  http://localhost:2024/docs"
echo "   Direct API: http://localhost:2024"
echo ""

# Force Chrome browser opening (NEVER use default Safari browser because of campatibility issues)
echo "🌐 Force opening in Chrome browser (ignoring Safari default)..."

CHROME_OPENED=false

# Check if Chrome is installed and force it to open
if command -v open >/dev/null 2>&1; then
    # macOS - Multiple Chrome detection methods
    if [ -d "/Applications/Google Chrome.app" ]; then
        echo "🎯 Found Chrome, forcing it to open..."
        open -a "Google Chrome" "$STUDIO_URL"
        echo "✅ Successfully forced Chrome to open (Safari ignored)"
        CHROME_OPENED=true
    elif [ -d "/Applications/Chromium.app" ]; then
        echo "🎯 Found Chromium, forcing it to open..."
        open -a "Chromium" "$STUDIO_URL"
        echo "✅ Successfully forced Chromium to open (Safari ignored)"
        CHROME_OPENED=true
    elif [ -d "/Users/$USER/Applications/Google Chrome.app" ]; then
        echo "🎯 Found Chrome in user directory, forcing it to open..."
        open -a "/Users/$USER/Applications/Google Chrome.app" "$STUDIO_URL"
        echo "✅ Successfully forced Chrome to open (Safari ignored)"
        CHROME_OPENED=true
    fi
elif command -v google-chrome >/dev/null 2>&1; then
    # Linux with Chrome
    echo "🎯 Found google-chrome command, forcing it to open..."
    google-chrome "$STUDIO_URL" &
    echo "✅ Successfully forced Chrome to open"
    CHROME_OPENED=true
elif command -v chromium-browser >/dev/null 2>&1; then
    # Linux with Chromium
    echo "🎯 Found chromium-browser command, forcing it to open..."
    chromium-browser "$STUDIO_URL" &
    echo "✅ Successfully forced Chromium to open"
    CHROME_OPENED=true
fi

# If Chrome not found, provide clear instructions (DO NOT open Safari)
if [ "$CHROME_OPENED" = false ]; then
    echo ""
    echo "🚫 Chrome/Chromium not found - Safari will NOT be opened automatically"
    echo "📥 Please install Google Chrome from: https://www.google.com/chrome/"
    echo "📋 Or manually copy this URL to Chrome:"
    echo "   $STUDIO_URL"
    echo ""
    echo "💡 Chrome provides the best LangGraph Studio experience!"
fi

echo ""
echo "🎯 Quick Start Commands:"
echo "   • Load dataset: 'Load the iris dataset'"
echo "   • Basic stats: 'Show me basic statistics'"
echo "   • Visualization: 'Create a scatter plot of sepal length vs width'"
echo "   • Correlation: 'Show correlation heatmap'"
echo ""
echo "🛑 To stop: pkill -f langgraph"
echo "📖 Full docs: See README.md"
echo ""

# Keep script running so user can see output
echo "Press Ctrl+C to stop the studio server..."
wait 