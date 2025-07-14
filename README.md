# Data Analysis AI Agent

An intelligent AI agent that translates natural language commands into executable Python code for dataset analysis. Built with LangGraph and OpenAI, this agent can analyze datasets, create visualizations, and perform machine learning tasks using simple English commands.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Configuration
Create a `config.py` file with your OpenAI API key:
```python
OPENAI_API_KEY = "your-api-key-here"
MODEL_NAME = "gpt-4-turbo-preview"
TEMPERATURE = 0.1
```

### 3. Start the Interactive CLI
```bash
python cli.py chat
```

This is the **main entry point** for the project. The CLI provides an interactive interface where you can:
- Ask natural language questions about your data
- Generate visualizations that automatically open in your browser
- View dataset information and analysis results

## 📁 Project Structure

```
├── cli.py                    # 🎯 MAIN ENTRY POINT - Interactive CLI
├── webview.py                # 🌐 Web server for visualization display
├── agent/
│   ├── __init__.py
│   └── data_analysis_agent.py  # LangGraph agent implementation
├── tools/
│   ├── __init__.py
│   └── dataset_tools.py        # Dataset operations & safe code execution
├── static/                    # 📊 Generated visualizations
├── data/                      # 📁 Dataset storage
├── config.py                  # ⚙️ Configuration settings
├── requirements.txt           # 📦 Python dependencies
├── test_agent.py             # 🧪 Comprehensive test suite
├── verification.ipynb         # 📓 Development notebook
└── README.md                 # 📖 This file
```

## 🔗 File Relationships & User Connection Points

### Primary User Interface
- **`cli.py`** ← **MAIN ENTRY POINT** for users
  - Provides interactive chat interface
  - Automatically starts web server for visualizations
  - Opens browser to display plots
  - Imports: `agent.data_analysis_agent`, `tools.dataset_tools`

### Core Components
- **`agent/data_analysis_agent.py`** ← LangGraph agent logic
  - Defines the AI agent workflow
  - Imports: `tools.dataset_tools`, `config`
  - Used by: `cli.py`, `test_agent.py`

- **`tools/dataset_tools.py`** ← Dataset operations & code execution
  - Safe Python code execution
  - Dataset loading and manipulation
  - Visualization generation
  - Used by: `agent/data_analysis_agent.py`

### Web Visualization
- **`webview.py`** ← Flask web server
  - Serves visualizations at `http://localhost:8080/`
  - Automatically started by CLI when visualizations are created
  - Displays plots from `static/last_plot.png`

### Configuration & Testing
- **`config.py`** ← API keys and settings
  - Used by: `agent/data_analysis_agent.py`
- **`test_agent.py`** ← Comprehensive testing
  - Tests all agent functionality
  - Used for: Development and debugging

## 🎯 How to Use

### Interactive Mode (Recommended)
```bash
python cli.py chat
```
Then ask questions like:
- "Load the iris dataset and show me basic statistics"
- "Create a scatter plot of sepal length vs sepal width"
- "Train a logistic regression model to predict species"

### Test the Agent
```bash
python test_agent.py
```

### Manual Web Server (if needed)
```bash
python webview.py
```
Then visit `http://localhost:8080/` in your browser.

## 🌟 Key Features

### Automatic Visualization Display
When you request a visualization:
1. **Agent generates the plot** using Python code
2. **Plot is saved** to `static/last_plot.png`
3. **Web server starts automatically** on port 8080
4. **Browser opens automatically** to display the plot
5. **No manual intervention required**

### Natural Language Interface
Ask for analysis in plain English:
- "Show me the distribution of petal width"
- "Create a correlation heatmap"
- "What's the mean sepal length by species?"
- "Train a model to predict species"

### Safe Code Execution
- Sandboxed Python execution
- Blocks dangerous operations
- Comprehensive error handling
- Input validation

## 🔧 Available Tools

The agent has access to these tools:

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

2. **Port 5000 in use (macOS)**
   - The project now uses port 8080 to avoid AirPlay conflicts
   - If you see port 5000 errors, update to use port 8080

3. **API Key Error**
   - Ensure `config.py` has your OpenAI API key
   - Check that the key is valid and has sufficient credits

4. **Browser doesn't open automatically**
   - The CLI will show the URL: `http://localhost:8080/`
   - Copy and paste it into your browser

### Debug Mode
```bash
python test_agent.py
```
This runs comprehensive tests to verify all functionality.

## 🔄 Development Workflow

1. **Make changes** to agent logic in `agent/data_analysis_agent.py`
2. **Update tools** in `tools/dataset_tools.py` if needed
3. **Test changes** with `python test_agent.py`
4. **Test CLI** with `python cli.py chat`
5. **Use verification.ipynb** for detailed development work

## 📈 Extending the Project

### Adding New Datasets
1. Add dataset loading function in `tools/dataset_tools.py`
2. Update the `load_dataset` tool in `agent/data_analysis_agent.py`
3. Test with the CLI

### Adding New Visualizations
1. Add visualization function in `tools/dataset_tools.py`
2. Update the `create_visualization` tool
3. Test with natural language commands

### Adding New Tools
1. Create the tool function in `tools/dataset_tools.py`
2. Add the tool decorator in `agent/data_analysis_agent.py`
3. Update the system prompt with tool description

## 📝 Example Workflow

1. **Start the CLI**: `python cli.py chat`
2. **Load data**: "Load the iris dataset"
3. **Explore**: "Show me basic statistics"
4. **Visualize**: "Create a correlation heatmap"
5. **Analyze**: "Train a model to predict species"
6. **View results**: Browser automatically opens to show plots

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `python test_agent.py`
5. Test with `python cli.py chat`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**🎯 Remember**: The main entry point is `python cli.py chat` - this gives you the full interactive experience with automatic visualization display! 