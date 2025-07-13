"""
LangGraph Studio integration for the Data Analysis AI Agent
This module provides the necessary components to visualize the agent workflow in LangGraph Studio.
"""

import json
from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import config
from tools.dataset_tools import dataset_tools

# Initialize the LLM
llm = ChatOpenAI(
    model=config.MODEL_NAME,
    temperature=config.TEMPERATURE,
    api_key=config.OPENAI_API_KEY
)

# Tool definitions (same as in data_analysis_agent.py)
@tool
def load_dataset(dataset_name: str = "iris") -> str:
    """Load a dataset for analysis. Currently supports 'iris' dataset."""
    if dataset_name.lower() == "iris":
        result = dataset_tools.load_iris_dataset()
        if result['success']:
            return json.dumps(result, indent=2)
        else:
            return f"Error loading dataset: {result['message']}"
    else:
        return f"Dataset '{dataset_name}' not supported yet. Please use 'iris'."

@tool
def get_dataset_info() -> str:
    """Get information about the currently loaded dataset."""
    result = dataset_tools.get_dataset_info()
    return json.dumps(result, indent=2)

@tool
def execute_code(code: str) -> str:
    """Execute Python code on the current dataset. The dataset is available as 'df'."""
    result = dataset_tools.execute_python_code(code)
    return json.dumps(result, indent=2)

@tool
def create_visualization(viz_type: str, **kwargs) -> str:
    """Create visualizations for the dataset. Supported types: correlation_heatmap, scatter_plot, histogram."""
    result = dataset_tools.create_visualization(viz_type, **kwargs)
    return json.dumps(result, indent=2)

@tool
def get_execution_history() -> str:
    """Get the history of executed code."""
    history = dataset_tools.get_execution_history()
    return json.dumps(history, indent=2)

# Create the tools list
tools = [load_dataset, get_dataset_info, execute_code, create_visualization, get_execution_history]

# Create the react agent for LangGraph Studio
memory = MemorySaver()
app = create_react_agent(llm, tools, checkpointer=memory)

def run_studio_agent(user_query: str) -> Dict[str, Any]:
    """Run the agent with a user query for LangGraph Studio."""
    # Create the system prompt
    system_prompt = """You are a data analysis AI agent that helps users analyze datasets using Python code.

Available tools:
- load_dataset: Load a dataset (currently supports 'iris')
- get_dataset_info: Get information about the current dataset
- execute_code: Execute Python code on the dataset (available as 'df')
- create_visualization: Create visualizations (correlation_heatmap, scatter_plot, histogram)
- get_execution_history: Get history of executed code

When the user asks for analysis, you should:
1. First load the dataset if not already loaded
2. Get dataset information to understand the structure
3. Write and execute Python code to perform the requested analysis
4. Create visualizations if requested
5. Provide clear explanations of your findings

IMPORTANT: For the Iris dataset, use these exact column names:
- 'sepal length (cm)' (not 'sepal_length')
- 'sepal width (cm)' (not 'sepal_width')
- 'petal length (cm)' (not 'petal_length')
- 'petal width (cm)' (not 'petal_width')
- 'species' (for the target column)

CRITICAL: Always use print() statements to display results. For example:
- Use: print(df['sepal width (cm)'].mean())
- NOT: df['sepal width (cm)'].mean()

This ensures the output is captured and displayed to the user.

Always write safe, well-documented Python code. The dataset is available as 'df' in your code.
Use pandas, numpy, matplotlib, seaborn, and scikit-learn for analysis."""

    # Run the agent
    result = app.invoke({
        "messages": [
            AIMessage(content=system_prompt),
            HumanMessage(content=user_query)
        ]
    })
    
    return {
        "final_messages": result["messages"],
        "user_query": user_query
    }

if __name__ == "__main__":
    # This will be used by LangGraph Studio
    print("LangGraph Studio integration ready!")
    print("Use 'langgraph dev' to start the studio")
    print("The workflow will be available at http://localhost:8123") 