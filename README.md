# Data Analysis AI Agent

An intelligent AI agent that translates natural language commands into executable Python code for dataset analysis. Built with LangGraph and OpenAI.

## 🔄 Workflow Logic

```
User Query → Agent → Tool Selection → Code Execution → Results → Visualization (optional)
     ↓              ↓           ↓               ↓            ↓
  Natural      LLM decides   Python code    Data output   Saved PNG
 Language      which tool    execution      displayed     file created
```

**Available Tools:**
- `load_dataset` → Load iris dataset
- `get_dataset_info` → Show dataset structure  
- `execute_code` → Run Python analysis code
- `create_visualization` → Generate charts/plots
- `get_execution_history` → View code history

## 🚀 Four Ways to Interact

### **1. 🎨 LangGraph Studio** (Visual Interface)
**Best for:** Interactive exploration, debugging, workflow visualization

```bash
./launch_studio.sh
```

**Features:**
- Visual graph of agent decision flow
- Real-time tool execution tracking
- State inspection and debugging
- Conversation history with context
- **Note:** Visualizations saved to `static/visualizations/` folder

**Quick Start Commands:**
```
• Load dataset: 'Load the iris dataset'
• Basic stats: 'Show me basic statistics'
• Visualization: 'Create a scatter plot of sepal length vs width'
• Correlation: 'Show correlation heatmap'
```

### **2. 💬 CLI Interface** (Command Line)
**Best for:** Quick analysis, scripting, automated workflows

```bash
# Interactive chat session
python interfaces/cli.py chat

# Run a quick test
python interfaces/cli.py test

# Run a demonstration
python interfaces/cli.py demo
```

**Features:**
- Direct conversation with agent
- Auto-opens visualizations in browser
- Faster for simple queries
- Good for automation/scripting

**Built-in Commands:**
- `quit` or `exit` - End the session
- `history` - Show execution history
- `info` - Show current dataset info
- `reset` - Reset to original dataset
- `help` - Show this help

### **3. 🤖 Agent Chat UI** (ChatGPT-like Interface)
**Best for:** Natural chat experience, web-based interface, sharing with others

```bash
./launch_agent_chat.sh
```

**Features:**
- ChatGPT-like chat interface
- Web-based, accessible from any browser
- Real-time streaming responses
- Conversation history and threading
- **Conversation summarization** to manage token usage
- **Token optimization** for tool outputs
- Works with deployed or local LangGraph server

**Setup Options:**
- **Deployed UI:** Use https://agentchat.vercel.app
- **Local UI:** Clone and run locally (requires Node.js)

**Configuration:**
```
Deployment URL: http://localhost:2024
Assistant ID: data_analysis_agent
LangSmith API Key: (optional for local development)
```

**Token Management:**
- **Automatic summarization** when conversation exceeds 8 messages

## 🏗️ Architecture Overview

The Data Analysis AI Agent uses a **client-server architecture** with multiple interaction interfaces. Here's how all components work together:

### **Core Architecture**

```
┌─────────────────┐    HTTP Requests    ┌─────────────────┐
│  Your Local     │ ←────────────────→ │  LangGraph      │
│  LangGraph      │                    │  Server         │
│  Server         │                    │  (Backend)      │
│ localhost:2024  │                    │                 │
└─────────────────┘                    └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │  Your Data      │
                                    │  Analysis       │
                                    │  Agent          │
                                    └─────────────────┘
```



### **Complete System Architecture**

```
┌─────────────────┐    HTTP Requests    ┌─────────────────┐
│  LangGraph      │ ←────────────────→ │                 │
│  Studio         │                    │                 │
│  (Debug UI)     │                    │                 │
│ smith.langchain │                    │                 │
│ .com/studio     │                    │                 │
└─────────────────┘                    │                 │
                                       │                 │
┌─────────────────┐    HTTP Requests    │  Your Local     │
│  Agent Chat     │ ←────────────────→ │  LangGraph      │
│  UI             │                    │  Server         │
│  (User UI)      │                    │  (Backend)      │
│ localhost:3000  │                    │ localhost:2024  │
└─────────────────┘                    │                 │
                                       │                 │
┌─────────────────┐    Direct Calls     │                 │
│  CLI Interface  │ ←────────────────→ │                 │
│  (Terminal)     │                    │                 │
└─────────────────┘                    │                 │
                                       │                 │
┌─────────────────┐    Direct Import    │                 │
│  Your Python    │ ←────────────────→ │                 │
│  Code           │                    │                 │
└─────────────────┘                    └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │  Your Data      │
                                    │  Analysis       │
                                    │  Agent          │
                                    └─────────────────┘
```

### **Key Benefits of This Architecture**

1. **Separation of Concerns**: UI separate from agent logic
2. **Multiple Access Points**: Different interfaces for different use cases
3. **Scalability**: Can deploy agent on different servers
4. **Development Flexibility**: Debug with Studio, use with Chat UI
5. **Integration Options**: Direct API calls or web interfaces

### **When to Use Each Interface**

| Interface | Best For | Use Case |
|-----------|----------|----------|
| **LangGraph Studio** | Development & Debugging | Testing agent logic, step-by-step debugging |
| **Agent Chat UI** | End-user Interaction | Natural language queries, web-based access |
| **CLI Interface** | Scripting & Automation | Batch processing, quick analysis |
| **Programmatic API** | Integration | Building custom applications |
- **Optimized tool outputs** to reduce token usage
- **Smart conversation history** to prevent context length issues

### **4. 🔧 Programmatic API** (Python Integration)
**Best for:** Integration into applications, custom workflows

```python
from agent.data_analysis_agent import run_agent, run_agent_with_state

# Simple query execution
result = run_agent("Load the iris dataset and show statistics")

# Stateful execution for Studio
state = run_agent_with_state("Create a scatter plot", initial_state=None)
```

**Features:**
- Direct Python API access
- State management for complex workflows
- Integration into larger applications
- Custom result processing

## ⚡ Quick Start

### 1. **Setup**
```bash
pip install -r requirements.txt
```

### 2. **Environment Variables**
Create `.env` file:
```bash
OPENAI_API_KEY=your-key-here
LANGCHAIN_API_KEY=your-langsmith-key  # Optional for tracing
```

### 3. **Choose Your Interface**

**🎨 For Visual Experience:**
```bash
./launch_studio.sh  # Opens Chrome with LangGraph Studio
```

**💬 For Quick Analysis:**
```bash
python interfaces/cli.py chat
```

**🤖 For Chat Experience:**
```bash
./launch_agent_chat.sh  # Starts LangGraph server + Agent Chat UI
```

**🔧 For Integration:**
```python
from agent.data_analysis_agent import run_agent
result = run_agent("Your query here")
```

## 📝 Example Queries

```
"Load the iris dataset and show me basic statistics"
"Create a scatter plot of sepal length vs sepal width colored by species"
"Show correlation between all features"
"Build a simple classification model"
"Train a logistic regression model to predict species"
```

## 📊 Output Locations

- **CLI Mode:** Visualizations auto-open in browser at `http://localhost:8080`
- **Studio Mode:** Images saved to `static/visualizations/` folder
- **Agent Chat UI:** Visualizations displayed in chat interface
- **Code History:** Available via `get_execution_history` tool

## 🏗️ Project Structure

```
├── agent/
│   └── data_analysis_agent.py    # Core unified agent
├── tools/
│   └── dataset_tools.py          # Data analysis tools  
├── interfaces/
│   ├── cli.py                    # Command line interface
│   ├── langgraph_app.py          # Studio integration
│   ├── agent_chat_ui.py          # Agent Chat UI integration
│   └── webview.py                # Web visualization server
├── static/visualizations/        # Generated plots
├── launch_studio.sh              # One-click Studio launcher
└── launch_agent_chat.sh          # Agent Chat UI launcher
```

## 🔧 Configuration

- **Default Dataset:** Iris (sklearn)
- **Supported Libraries:** pandas, numpy, matplotlib, seaborn, plotly, scikit-learn
- **Python Environment:** Uses safe code execution with pre-loaded libraries

## 🎯 When to Use Each Interface

| Scenario | Interface | Why |
|----------|-----------|-----|
| Learning agent behavior | Studio | Visual workflow tracking |
| Debugging complex queries | Studio | State inspection |
| Quick data analysis | CLI | Faster startup |
| Batch processing | CLI | Better for scripting |
| Presentation/demos | Studio | Visual appeal |
| Automated workflows | CLI | Command line friendly |
| Natural chat experience | Agent Chat UI | ChatGPT-like interface |
| Web-based sharing | Agent Chat UI | Accessible from any browser |
| Integration into apps | Programmatic API | Direct Python access |
| Custom result processing | Programmatic API | Full control over output | 