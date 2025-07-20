# Agent Chat UI Integration

This document describes the integration of our Data Analysis AI Agent with the LangChain Agent Chat UI, providing a ChatGPT-like interface for data analysis.

## Overview

The Agent Chat UI integration provides a web-based chat interface that allows users to interact with our data analysis agent through natural language, similar to ChatGPT. The integration includes advanced token management features to handle long conversations efficiently.

## Features

### 🤖 ChatGPT-like Interface
- **Natural conversation flow** with message threading
- **Real-time streaming responses** as the agent processes requests
- **Web-based interface** accessible from any browser
- **Conversation history** maintained across sessions

### 📊 Data Analysis Capabilities
- **Dataset loading and exploration** (Iris dataset)
- **Statistical analysis** with descriptive statistics
- **Visualization creation** (scatter plots, heatmaps, etc.)
- **Machine learning** (classification, regression models)
- **Code execution** with safe Python environment

### 🧠 Smart Token Management
- **Automatic conversation summarization** when messages exceed 8
- **Optimized tool outputs** to reduce token usage
- **Smart conversation history** to prevent context length issues
- **Token usage monitoring** and optimization

## Setup Instructions

### Option 1: Deployed UI (Recommended)

1. **Start the LangGraph server:**
   ```bash
   ./launch_agent_chat.sh
   ```

2. **Open the Agent Chat UI:**
   - Go to https://agentchat.vercel.app
   - Enter the configuration:
     - **Deployment URL:** `http://localhost:2024`
     - **Assistant ID:** `data_analysis_agent`
     - **LangSmith API Key:** (leave empty for local development)

3. **Start chatting!**

### Option 2: Local UI

1. **Prerequisites:**
   - Node.js installed
   - pnpm package manager

2. **Run the setup script:**
   ```bash
   ./launch_agent_chat.sh
   ```
   - Choose "y" when prompted to run locally
   - The script will clone and set up the Agent Chat UI automatically

3. **Access the interface:**
   - Open http://localhost:3000 in your browser
   - The configuration will be pre-filled

## Configuration

### Environment Variables

For local development, the following environment variables are set automatically:

```bash
NEXT_PUBLIC_API_URL=http://localhost:2024
NEXT_PUBLIC_ASSISTANT_ID=data_analysis_agent
```

### LangGraph Server Configuration

The LangGraph server runs on `http://localhost:2024` and provides:
- **API endpoints** for the Agent Chat UI
- **Tool execution** for data analysis
- **State management** for conversation history

## Token Management

### Conversation Summarization

The integration automatically summarizes conversations when they exceed 8 messages to prevent token limit issues:

```python
# Automatic summarization trigger
if len(messages) > 8:
    # Summarize previous exchanges
    summary = summarize_conversation(messages)
    # Replace with summary + current query
```

### Tool Output Optimization

Tool outputs are optimized to reduce token usage:

- **Dataset info:** Only essential statistics included
- **Visualizations:** File paths instead of base64 data
- **Code execution:** Concise output formatting
- **Error messages:** Simplified error reporting

### Token Usage Monitoring

The system monitors token usage and applies optimizations:
- **Message count tracking**
- **Automatic summarization**
- **Tool output compression**
- **Context length management**

## Example Conversations

### Basic Data Analysis
```
User: Load the iris dataset and show me basic statistics
Assistant: I've loaded the Iris dataset with 150 rows and 6 columns. Here are the basic statistics...

User: Create a scatter plot of sepal length vs sepal width
Assistant: I've created a scatter plot showing the relationship between sepal length and width...
```

### Advanced Analysis
```
User: Show correlation between all features
Assistant: Here's the correlation matrix for the numeric features...

User: Train a logistic regression model to predict species
Assistant: I've trained a logistic regression model with 96% accuracy...
```

## Troubleshooting

### Common Issues

1. **"Connection refused" error:**
   - Ensure the LangGraph server is running: `./launch_agent_chat.sh`
   - Check that port 2024 is available

2. **"Context length exceeded" error:**
   - The conversation summarization should handle this automatically
   - Try starting a new conversation if issues persist

3. **"Assistant not found" error:**
   - Verify the Assistant ID is set to `data_analysis_agent`
   - Check the LangGraph server logs

4. **Visualizations not displaying:**
   - Check that the static/visualizations directory exists
   - Verify file permissions for image saving

### Debug Mode

To enable debug logging:

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_PROJECT=data-analysis-agent
./launch_agent_chat.sh
```

## Architecture

### Components

1. **Agent Chat UI Wrapper** (`interfaces/agent_chat_ui.py`)
   - Manages conversation state
   - Handles token optimization
   - Provides summarization

2. **Conversation Summarizer** (`ConversationSummarizer`)
   - Monitors message count
   - Generates conversation summaries
   - Manages token usage

3. **Optimized Dataset Tools** (`tools/dataset_tools.py`)
   - Reduced token output
   - Essential information only
   - Efficient data handling

### Data Flow

```
User Query → Agent Chat UI → LangGraph Server → Tool Execution → Optimized Response → Chat Interface
```

## Performance Optimization

### Token Usage Strategies

1. **Conversation Summarization:**
   - Triggers at 8+ messages
   - Preserves essential context
   - Reduces token count by ~40%

2. **Tool Output Optimization:**
   - Minimal JSON responses
   - File paths instead of data
   - Concise error messages

3. **Smart History Management:**
   - Keeps system message
   - Maintains current query
   - Summarizes past exchanges

### Monitoring

The system provides feedback on token management:
- Summarization notifications
- Token usage estimates
- Optimization status

## Future Enhancements

### Planned Features

1. **Advanced Summarization:**
   - Domain-specific summarization
   - Multi-level conversation compression
   - Context-aware summarization

2. **Enhanced Visualizations:**
   - Interactive plot embedding
   - Real-time plot updates
   - Plot sharing capabilities

3. **Extended Tool Support:**
   - Additional datasets
   - More analysis types
   - Custom tool integration

### Integration Improvements

1. **Better Error Handling:**
   - Graceful degradation
   - User-friendly error messages
   - Automatic recovery

2. **Performance Monitoring:**
   - Real-time token tracking
   - Response time optimization
   - Usage analytics

## Support

For issues or questions:

1. **Check the logs:** Look for error messages in the terminal
2. **Verify configuration:** Ensure all environment variables are set
3. **Test connectivity:** Verify the LangGraph server is accessible
4. **Review token usage:** Monitor conversation length and summarization

The Agent Chat UI integration provides a powerful, user-friendly interface for data analysis while maintaining efficient token usage through smart conversation management. 