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

## 🚀 Usage Scenarios

### **🎨 LangGraph Studio** (Visual Interface)
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

### **💬 CLI Interface** (Command Line)
**Best for:** Quick analysis, scripting, automated workflows

```bash
python interfaces/cli.py chat
```

**Features:**
- Direct conversation with agent
- Auto-opens visualizations in browser
- Faster for simple queries
- Good for automation/scripting

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

### 3. **Choose Interface**

**Interactive Visual Experience:**
```bash
./launch_studio.sh  # Opens Chrome with LangGraph Studio
```

**Quick CLI Chat:**
```bash
python interfaces/cli.py chat
```

## 📝 Example Queries

```
"Load the iris dataset and show me basic statistics"
"Create a scatter plot of sepal length vs sepal width colored by species"
"Show correlation between all features"
"Build a simple classification model"
```

## 📊 Output Locations

- **CLI Mode:** Visualizations auto-open in browser
- **Studio Mode:** Images saved to `static/visualizations/` folder
- **Code History:** Available via `get_execution_history` tool

## 🏗️ Project Structure

```
├── agent/
│   └── data_analysis_agent.py    # Core unified agent
├── tools/
│   └── dataset_tools.py          # Data analysis tools  
├── interfaces/
│   ├── cli.py                    # Command line interface
│   └── langgraph_app.py          # Studio integration
├── static/visualizations/        # Generated plots
└── launch_studio.sh              # One-click Studio launcher
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