#!/bin/bash

# LangChain Agent Chat UI Launcher
# Quick script to start LangGraph server and Agent Chat UI

echo "🚀 Starting Data Analysis Agent Chat UI..."

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
sleep 3

# Start LangGraph server locally
echo "🌐 Starting LangGraph server..."
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
        break
    fi
    echo "   Attempt $i/8: Waiting for server..."
    sleep 2
done

if ! curl -s --max-time 2 "$LOCAL_URL/openapi.json" > /dev/null 2>&1; then
    echo "❌ Server failed to start. Check error messages above."
    exit 1
fi

echo ""
echo "🎯 Agent Chat UI Configuration:"
echo "   Deployment URL: $LOCAL_URL"
echo "   Assistant ID: data_analysis_agent"
echo "   LangSmith API Key: (optional for local development)"
echo ""

echo "🌐 Agent Chat UI Options:"
echo "   1. Use the deployed site: https://agentchat.vercel.app"
echo "   2. Run locally (requires Node.js and pnpm)"
echo ""

# Check if Node.js and pnpm are available for local setup
if command -v node >/dev/null 2>&1 && command -v pnpm >/dev/null 2>&1; then
    echo "📦 Node.js and pnpm detected. Would you like to run Agent Chat UI locally?"
    echo "   This will clone the repository and start the local development server."
    echo ""
    read -p "Run locally? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 Setting up Agent Chat UI locally..."
        
        # Check if agent-chat-ui directory exists
        if [ ! -d "agent-chat-ui" ]; then
            echo "📥 Cloning Agent Chat UI repository..."
            git clone https://github.com/langchain-ai/agent-chat-ui.git
        fi
        
        cd agent-chat-ui
        
        # Install dependencies
        echo "📦 Installing dependencies..."
        pnpm install
        
        # Create .env file with our configuration
        echo "⚙️  Creating configuration..."
        cat > .env << EOF
NEXT_PUBLIC_API_URL=http://localhost:2024
NEXT_PUBLIC_ASSISTANT_ID=data_analysis_agent
EOF
        
        echo "✅ Configuration created!"
        echo "   NEXT_PUBLIC_API_URL=http://localhost:2024"
        echo "   NEXT_PUBLIC_ASSISTANT_ID=data_analysis_agent"
        echo ""
        
        # Start the development server
        echo "🌐 Starting Agent Chat UI..."
        echo "   The chat interface will be available at: http://localhost:3000"
        echo ""
        pnpm dev &
        
        # Wait a moment for the server to start
        sleep 5
        
        # Force Chrome browser opening (NEVER use default Safari browser)
        echo "🌐 Force opening in Chrome browser (ignoring Safari default)..."
        
        CHROME_OPENED=false
        
        # Check if Chrome is installed and force it to open
        if command -v open >/dev/null 2>&1; then
            # macOS - Multiple Chrome detection methods
            if [ -d "/Applications/Google Chrome.app" ]; then
                echo "🎯 Found Chrome, forcing it to open..."
                open -a "Google Chrome" "http://localhost:3000"
                echo "✅ Successfully forced Chrome to open (Safari ignored)"
                CHROME_OPENED=true
            elif [ -d "/Applications/Chromium.app" ]; then
                echo "🎯 Found Chromium, forcing it to open..."
                open -a "Chromium" "http://localhost:3000"
                echo "✅ Successfully forced Chromium to open (Safari ignored)"
                CHROME_OPENED=true
            elif [ -d "/Users/$USER/Applications/Google Chrome.app" ]; then
                echo "🎯 Found Chrome in user directory, forcing it to open..."
                open -a "/Users/$USER/Applications/Google Chrome.app" "http://localhost:3000"
                echo "✅ Successfully forced Chrome to open (Safari ignored)"
                CHROME_OPENED=true
            fi
        elif command -v google-chrome >/dev/null 2>&1; then
            # Linux with Chrome
            echo "🎯 Found google-chrome command, forcing it to open..."
            google-chrome "http://localhost:3000" &
            echo "✅ Successfully forced Chrome to open"
            CHROME_OPENED=true
        elif command -v chromium-browser >/dev/null 2>&1; then
            # Linux with Chromium
            echo "🎯 Found chromium-browser command, forcing it to open..."
            chromium-browser "http://localhost:3000" &
            echo "✅ Successfully forced Chromium to open"
            CHROME_OPENED=true
        fi
        
        # If Chrome not found, provide clear instructions (DO NOT open Safari)
        if [ "$CHROME_OPENED" = false ]; then
            echo ""
            echo "🚫 Chrome/Chromium not found - Safari will NOT be opened automatically"
            echo "📥 Please install Google Chrome from: https://www.google.com/chrome/"
            echo "📋 Or manually copy this URL to Chrome:"
            echo "   http://localhost:3000"
            echo ""
            echo "💡 Chrome provides the best Agent Chat UI experience!"
        fi
        
        echo ""
        echo "🎯 Quick Start Commands for the Chat Interface:"
        echo "   • Load dataset: 'Load the iris dataset'"
        echo "   • Basic stats: 'Show me basic statistics'"
        echo "   • Visualization: 'Create a scatter plot of sepal length vs width'"
        echo "   • Correlation: 'Show correlation heatmap'"
        echo ""
        echo "🛑 To stop: pkill -f langgraph && pkill -f next"
        echo ""
        
        # Keep script running
        echo "Press Ctrl+C to stop all servers..."
        wait
        
    else
        echo ""
        echo "🌐 To use the deployed Agent Chat UI:"
        echo "   1. Go to: https://agentchat.vercel.app"
        echo "   2. Enter these settings:"
        echo "      - Deployment URL: $LOCAL_URL"
        echo "      - Assistant ID: data_analysis_agent"
        echo "      - LangSmith API Key: (leave empty for local development)"
        echo "   3. Click 'Continue' to start chatting!"
        echo ""
        echo "🛑 To stop LangGraph server: pkill -f langgraph"
        echo ""
        echo "Press Ctrl+C to stop the LangGraph server..."
        wait
    fi
else
    echo "📦 Node.js or pnpm not found. Using deployed Agent Chat UI..."
    echo ""
    echo "🌐 To use the deployed Agent Chat UI:"
    echo "   1. Go to: https://agentchat.vercel.app"
    echo "   2. Enter these settings:"
    echo "      - Deployment URL: $LOCAL_URL"
    echo "      - Assistant ID: data_analysis_agent"
    echo "      - LangSmith API Key: (leave empty for local development)"
    echo "   3. Click 'Continue' to start chatting!"
    echo ""
    echo "🛑 To stop LangGraph server: pkill -f langgraph"
    echo ""
    echo "Press Ctrl+C to stop the LangGraph server..."
    wait
fi 