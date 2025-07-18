# Data Analysis AI Agent

An intelligent AI agent that translates natural language commands into executable Python code for dataset analysis. Built with LangGraph and OpenAI, this agent can analyze datasets, create visualizations, and perform machine learning tasks using simple English commands.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Configuration
Create a `.env` file with your API keys:
```bash
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here
MODEL_NAME=gpt-4o-mini
TEMPERATURE=0.1

# LangSmith Configuration for tracing (optional)
LANGSMITH_API_KEY=your-langsmith-api-key-here
LANGSMITH_PROJECT=data-analysis-agent
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

### 3. Start the Interactive CLI
```bash
python interfaces/cli.py chat
```

This is the **main entry point** for the project. The CLI provides an interactive interface where you can:
- Ask natural language questions about your data
- Generate visualizations that automatically open in your browser
- View dataset information and analysis results

## 📁 Project Structure

```
├── interfaces/                # 🎯 USER INTERFACES
│   ├── __init__.py
│   ├── cli.py                # 💬 MAIN ENTRY POINT - Interactive CLI
│   ├── webview.py            # 🌐 Web server for visualization display
│   └── langgraph_app.py      # 🎨 LangGraph Studio integration
├── agent/                    # 🧠 CORE AGENT
│   ├── __init__.py
│   └── data_analysis_agent.py  # Unified agent implementation
├── tools/                    # 🔧 DATA TOOLS
│   ├── __init__.py
│   └── dataset_tools.py        # Dataset operations & safe code execution
├── tests/                    # 🧪 TESTING
│   ├── __init__.py
│   └── test_unified_agent.py  # Comprehensive test suite
├── static/                    # 📊 Generated visualizations
├── data/                      # 📁 Dataset storage
├── config.py                  # ⚙️ Configuration settings
├── requirements.txt           # 📦 Python dependencies
├── verification.ipynb         # 📓 Development notebook
└── README.md                 # 📖 This file
```

## 🔗 Unified Agent Architecture

### **Single Agent, Multiple Interfaces**

The project now uses a **unified agent architecture** that supports both CLI and LangGraph Studio:

#### **Core Agent: `agent/data_analysis_agent.py`**
- **Unified Implementation**: Single agent for all interfaces
- **Dual Interfaces**: CLI and Studio compatibility
- **State Management**: Rich state tracking for Studio visualization
- **Backward Compatibility**: Existing CLI users unaffected

#### **Interface Options**

| Interface | Usage | Features |
|-----------|-------|----------|
| **CLI** | `python cli.py chat` | Interactive chat, auto-browser |
| **Studio** | `python langgraph_app.py` | Full state visualization |
| **Programmatic** | `run_agent(query)` | Direct Python integration |

### **State Management**

The unified agent tracks rich state information:

```python
class AgentState(TypedDict):
    messages: List[BaseMessage]          # Conversation history
    user_query: str                      # Current query
    dataset_loaded: bool                 # Dataset status
    dataset_info: Optional[Dict]         # Dataset metadata
    execution_history: List[Dict]        # Code execution history
    current_step: str                    # Workflow progress
```

## 🎯 How to Use

### Interactive Mode (Recommended)
```bash
python interfaces/cli.py chat
```
Then ask questions like:
- "Load the iris dataset and show me basic statistics"
- "Create a scatter plot of sepal length vs sepal width"
- "Train a logistic regression model to predict species"

### LangGraph Studio Integration
```bash
python interfaces/langgraph_app.py
```
Then use in LangGraph Studio for:
- **Workflow Visualization**: See the agent's decision-making process
- **State Tracking**: Monitor dataset loading, code execution, and results
- **Debugging**: Step-by-step execution analysis

### Programmatic Usage
```python
from agent.data_analysis_agent import run_agent, run_agent_with_state

# CLI-style usage
result = run_agent("Load iris dataset and show statistics")

# Studio-style usage with state management
state = run_agent_with_state("Create correlation heatmap", state)
```

### Test the Unified Agent
```bash
python tests/test_unified_agent.py
```

### Manual Web Server (if needed)
```bash
python interfaces/webview.py
```
Then visit `http://localhost:8080/` in your browser.

## 🌟 Key Features

### **Unified Architecture**
- **Single Agent**: One implementation for all interfaces
- **Dual Compatibility**: Works with CLI and LangGraph Studio
- **State Persistence**: Maintains context across interactions
- **Tool Consistency**: Same tools available everywhere

### **Automatic Visualization Display**
When you request a visualization:
1. **Agent generates the plot** using Python code
2. **Plot is saved** to `static/last_plot.png`
3. **Web server starts automatically** on port 8080
4. **Browser opens automatically** to display the plot
5. **No manual intervention required**

### **Natural Language Interface**
Ask for analysis in plain English:
- "Show me the distribution of petal width"
- "Create a correlation heatmap"
- "What's the mean sepal length by species?"
- "Train a model to predict species"

### **Safe Code Execution**
- Sandboxed Python execution
- Blocks dangerous operations
- Comprehensive error handling
- Input validation

### **Rich State Tracking**
- **Dataset Status**: Track loading and modification
- **Execution History**: Log all code executions
- **Workflow Progress**: Monitor current step
- **Tool Usage**: Track which tools were called

## 🔧 Available Tools

The unified agent has access to these tools:

- **`load_dataset`**: Load datasets (currently supports 'iris')
- **`get_dataset_info`**: Get dataset information and statistics
- **`execute_code`**: Execute Python code on the dataset (available as 'df')
- **`create_visualization`**: Generate plots with matplotlib/seaborn
- **`get_execution_history`**: View history of executed code

## 📊 Supported Operations

### Data Analysis
- Load and explore datasets
- Calculate statistics and summaries
- Filter and sort data
- Handle missing values

### Visualizations
- Correlation heatmaps
- Scatter plots
- Histograms and distributions
- Custom matplotlib/seaborn plots

### Machine Learning
- Data preprocessing
- Model training (Logistic Regression, Random Forest)
- Model evaluation and metrics
- Predictions and classifications

## 🛠️ Troubleshooting

### Common Issues

1. **"No module named 'flask'"**
   ```bash
   pip install flask
   ```

2. **API Key Error**
   - Ensure `.env` file has your OpenAI API key
   - Check that the key is valid and has sufficient credits
   - Set environment variable: `export OPENAI_API_KEY="your-key"`

3. **Browser doesn't open automatically**
   - The CLI will show the URL: `http://localhost:8080/`
   - Copy and paste it into your browser

4. **Port 8080 in use**
   - The project uses port 8080 to avoid AirPlay conflicts
   - If you see port conflicts, check for other services

### Debug Mode
```bash
python tests/test_unified_agent.py
```
This runs comprehensive tests to verify all functionality.

## 🔄 Development Workflow

### **Unified Development**
1. **Make changes** to agent logic in `agent/data_analysis_agent.py`
2. **Update tools** in `tools/dataset_tools.py` if needed
3. **Test changes** with `python tests/test_unified_agent.py`
4. **Test CLI** with `python interfaces/cli.py chat`
5. **Test Studio** with `python interfaces/langgraph_app.py`
6. **Use verification.ipynb** for detailed development work

### **State Management**
The unified agent maintains state across interactions:
- **Dataset Loading**: Tracks when datasets are loaded
- **Execution History**: Logs all code executions with timestamps
- **Workflow Progress**: Monitors current step in the process
- **Tool Usage**: Records which tools were called and when

## 🔍 LangGraph Studio Integration

### **Studio Features**
- **Workflow Visualization**: See the agent's decision-making process
- **State Tracking**: Monitor dataset loading, code execution, and results
- **Tool Execution**: View each tool call with inputs and outputs
- **Debug Information**: Detailed logs for troubleshooting
- **Performance Metrics**: Track response times and token usage

### **How to Use with Studio**
1. **Run the app**: `python langgraph_app.py`
2. **Open Studio**: Visit [LangGraph Studio](https://studio.langchain.com/)
3. **Load the app**: Import the `langgraph_app.py` file
4. **Interact**: Use the Studio interface to test queries
5. **Visualize**: See the full workflow with state tracking

### **Studio State Visualization**
When you run a query in Studio, you'll see:
- **Tool Calls**: Each dataset operation and code execution
- **State Changes**: How the agent's state evolves
- **Message Flow**: Complete conversation history
- **Execution Path**: Step-by-step decision making

## 📈 Extending the Project

### **Adding New Datasets**
1. Add dataset loading function in `tools/dataset_tools.py`
2. Update the `load_dataset` tool in `agent/data_analysis_agent.py`
3. Test with both CLI and Studio interfaces

### **Adding New Visualizations**
1. Add visualization function in `tools/dataset_tools.py`
2. Update the `create_visualization` tool
3. Test with natural language commands

### **Adding New Tools**
1. Create the tool function in `tools/dataset_tools.py`
2. Add the tool decorator in `agent/data_analysis_agent.py`
3. Update the system prompt with tool description
4. Test with both interfaces

### **Adding New Interfaces**
The unified architecture makes it easy to add new interfaces:
1. Import the unified agent: `from agent.data_analysis_agent import app`
2. Create your interface wrapper
3. Use the same tools and state management

## 📝 Example Workflow

### **CLI Workflow**
```bash
# Start the CLI
python interfaces/cli.py chat

# Interactive session
> Load the iris dataset
> Show me basic statistics
> Create a correlation heatmap
> Train a model to predict species
```

### **Studio Workflow**
```bash
# Start the Studio app
python interfaces/langgraph_app.py

# In LangGraph Studio
1. Load the app
2. Send queries through Studio interface
3. Visualize the workflow and state changes
4. Debug and analyze the agent's behavior
```

### **Programmatic Workflow**
```python
from agent.data_analysis_agent import run_agent, run_agent_with_state

# Simple usage
result = run_agent("Load iris and show statistics")

# State-aware usage
state = run_agent_with_state("Load dataset")
state = run_agent_with_state("Show statistics", state)
state = run_agent_with_state("Create plot", state)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes to the unified agent
4. Test with `python test_unified_agent.py`
5. Test CLI with `python cli.py chat`
6. Test Studio with `python langgraph_app.py`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**🎯 Remember**: The unified agent architecture provides a single, maintainable implementation that works seamlessly with both CLI and LangGraph Studio interfaces! 