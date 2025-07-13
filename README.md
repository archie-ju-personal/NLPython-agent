# Data Analysis AI Agent

An intelligent AI agent that translates natural language commands into executable Python code for dataset analysis. Built with LangGraph and OpenAI, this agent can analyze datasets, create visualizations, and perform machine learning tasks using simple English commands.

## Features

- **Natural Language Interface**: Ask for data analysis in plain English
- **Safe Code Execution**: Secure Python code execution with safety checks
- **Multiple Dataset Support**: Currently supports Iris dataset, extensible for others
- **Rich Visualizations**: Create correlation heatmaps, scatter plots, histograms
- **Machine Learning**: Train models and perform predictions
- **LangGraph Studio Integration**: Visualize and monitor agent workflow
- **Interactive CLI**: Test and interact with the agent directly

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test the Agent

```bash
# Run a quick test
python cli.py test

# Start interactive chat
python cli.py chat

# Run a full demonstration
python cli.py demo
```

### 3. Example Queries

Try these natural language commands:

```bash
# Load and explore the dataset
"Load the iris dataset and show me basic statistics"

# Create visualizations
"Create a correlation heatmap"
"Show me a scatter plot of sepal length vs sepal width"

# Machine learning
"Train a logistic regression model to predict species"

# Data analysis
"Show me the distribution of petal length by species"
"Calculate the mean and standard deviation of all numeric columns"
```

## Project Structure

```
├── agent/
│   └── data_analysis_agent.py    # Main LangGraph agent
├── tools/
│   └── dataset_tools.py          # Dataset operations and code execution
├── cli.py                        # Interactive CLI interface
├── langgraph_studio.py           # LangGraph Studio integration
├── config.py                     # Configuration settings
├── requirements.txt              # Python dependencies
└── README.md                    # This file
```

## LangGraph Studio Integration

To visualize your agent workflow in LangGraph Studio:

1. **Install LangGraph CLI**:
   ```bash
   pip install langgraph-cli
   ```

2. **Start LangGraph Studio**:
   ```bash
   langgraph dev langgraph_studio.py
   ```

3. **Access the Studio**:
   Open your browser to `http://localhost:8123` to see the agent workflow visualization.

## Available Tools

The agent has access to these tools:

- **`load_dataset`**: Load a dataset (currently supports 'iris')
- **`get_dataset_info`**: Get information about the current dataset
- **`execute_code`**: Execute Python code on the dataset (available as 'df')
- **`create_visualization`**: Create visualizations (correlation_heatmap, scatter_plot, histogram)
- **`get_execution_history`**: Get history of executed code

## Security Features

- **Code Safety**: Blocks dangerous operations like file system access, imports, etc.
- **Sandboxed Execution**: Code runs in a controlled environment
- **Input Validation**: All inputs are validated before execution
- **Error Handling**: Comprehensive error handling and reporting

## Supported Operations

### Data Loading and Exploration
- Load datasets
- View basic statistics
- Check data types and missing values
- Display sample data

### Visualizations
- Correlation heatmaps
- Scatter plots
- Histograms
- Custom matplotlib/seaborn plots

### Machine Learning
- Data preprocessing
- Model training (Logistic Regression, Random Forest)
- Model evaluation
- Predictions

### Data Manipulation
- Filtering and sorting
- Aggregations
- Feature engineering
- Data cleaning

## Example Workflow

1. **Load Dataset**: "Load the iris dataset"
2. **Explore Data**: "Show me basic information about the dataset"
3. **Create Visualization**: "Create a correlation heatmap"
4. **Train Model**: "Train a logistic regression model to predict species"
5. **Evaluate**: "Show me the model accuracy and classification report"

## Extending the Agent

### Adding New Datasets

1. Add dataset loading function in `tools/dataset_tools.py`
2. Update the `load_dataset` tool in the agent
3. Test with the CLI

### Adding New Tools

1. Create the tool function in `tools/dataset_tools.py`
2. Add the tool decorator in the agent
3. Update the system prompt with tool description

### Adding New Visualizations

1. Add visualization function in `tools/dataset_tools.py`
2. Update the `create_visualization` tool
3. Test with natural language commands

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your OpenAI API key is set in `config.py`
2. **Import Errors**: Install all dependencies with `pip install -r requirements.txt`
3. **Code Execution Errors**: Check that your code doesn't use restricted operations
4. **Memory Issues**: Large datasets may require more memory

### Debug Mode

Run the agent with verbose output:

```python
from agent.data_analysis_agent import run_agent
result = run_agent("Your query here")
print(json.dumps(result, indent=2))
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the example queries
3. Test with the CLI interface
4. Open an issue on GitHub 