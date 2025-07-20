import json
from typing import Dict, Any, List, Optional, Annotated, Sequence
import operator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START, MessagesState
import config
from tools.dataset_tools import dataset_tools
import os

# Set up LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = config.LANGSMITH_API_KEY
os.environ["LANGCHAIN_PROJECT"] = config.LANGSMITH_PROJECT
os.environ["LANGCHAIN_ENDPOINT"] = config.LANGSMITH_ENDPOINT

# Initialize the LLM
llm = ChatOpenAI(
    model=config.MODEL_NAME,
    temperature=config.TEMPERATURE,
    api_key=config.OPENAI_API_KEY
)

# Tool definitions
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
    # Ensure we return a proper JSON string
    return json.dumps(result, indent=2, default=str)

@tool
def create_visualization(code: str) -> str:
    """Execute Python code to create a visualization. The code should generate a plot using matplotlib/seaborn/plotly, and the resulting image will be returned as PNG bytes."""
    import base64
    result = dataset_tools.create_visualization(code)
    if result['success'] and 'plot_data' in result:
        # Convert bytes to base64 string for JSON serialization
        result['plot_data'] = base64.b64encode(result['plot_data']).decode('utf-8')
    return json.dumps(result, indent=2)

@tool
def get_execution_history() -> str:
    """Get the history of executed code."""
    history = dataset_tools.get_execution_history()
    return json.dumps(history, indent=2)

# Create the tools list
tools = [load_dataset, get_dataset_info, execute_code, create_visualization, get_execution_history]

# System prompt for the agent
SYSTEM_PROMPT = """You are a data analysis AI agent that helps users analyze datasets using Python code.

Available tools:
- load_dataset: Load a dataset (currently supports 'iris')
- get_dataset_info: Get information about the current dataset
- execute_code: Execute Python code on the dataset (available as 'df')
- create_visualization: Execute Python code to create a visualization (provide the code as a string; the code should generate a plot using matplotlib/seaborn/plotly, and the resulting image will be returned as PNG bytes)
- get_execution_history: Get history of executed code

When the user asks for analysis, you should:
1. First load the dataset if not already loaded
2. Get dataset information to understand the structure
3. Write and execute Python code to perform the requested analysis
4. Write and execute Python code to create visualizations if requested (using the create_visualization tool)
5. Provide clear explanations of your findings

CRITICAL: Always use print() statements to display results. For example:
- Use: print(df['column_name'].mean())
- NOT: df['column_name'].mean()

IMPORTANT: You can use import statements for any library you need. Common libraries are pre-loaded:
- pandas (pd), numpy (np), matplotlib (plt), seaborn (sns), plotly (px, go), scikit-learn
- You can also import additional libraries as needed

Always write safe, well-documented Python code. The dataset is available as 'df' in your code.
Use the pre-loaded libraries: pandas (pd), numpy (np), matplotlib (plt), seaborn (sns), plotly (px, go), and scikit-learn."""

# Create a mapping of tool names to tool functions
tools_by_name = {tool.name: tool for tool in tools}

# Bind tools to the LLM
llm_with_tools = llm.bind_tools(tools)

# Define the agent function
def call_model(state: MessagesState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# Define the tool function
def call_tool(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    
    tool_messages = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_input = tool_call["args"]
        
        # Get the tool function
        tool_func = tools_by_name[tool_name]
        
        try:
            # Call the tool
            result = tool_func.invoke(tool_input)
        except Exception as e:
            result = f"Error calling tool {tool_name}: {str(e)}"
        
        # Create tool message
        tool_message = ToolMessage(
            content=str(result),
            name=tool_name,
            tool_call_id=tool_call["id"],
        )
        tool_messages.append(tool_message)

    return {"messages": tool_messages}

# Define condition for calling tools
def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    # If there are no tool calls, then we finish
    if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
        return END
    else:
        return "tools"

# Build the graph
workflow = StateGraph(MessagesState)

# Add the agent node
workflow.add_node("agent", call_model)
workflow.add_node("tools", call_tool)

# Set the entrypoint
workflow.add_edge(START, "agent")

# Add conditional edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END,
    }
)

# Add edge from tools to agent
workflow.add_edge("tools", "agent")

# Compile the workflow
app = workflow.compile()

def run_agent(user_query: str) -> Dict[str, Any]:
    """
    Run the agent with a user query (CLI interface).
    Maintains backward compatibility with existing CLI.
    """
    # Run the agent
    result = app.invoke({
        "messages": [
            AIMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_query)
        ]
    })
    
    return {
        "final_messages": result["messages"],
        "user_query": user_query
    }

# Legacy state definition for backward compatibility
from typing_extensions import TypedDict

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]
    user_query: Annotated[str, "The user's query"]
    dataset_loaded: Annotated[bool, "Whether a dataset is loaded"]
    dataset_info: Annotated[Optional[Dict], "Dataset information"]
    execution_history: Annotated[List[Dict], "History of executed code"]
    current_step: Annotated[str, "Current step in the workflow"]

def run_agent_with_state(user_query: str, initial_state: Optional[AgentState] = None) -> AgentState:
    """
    Run the agent with state management (Studio interface).
    Returns full state for LangGraph Studio visualization.
    """
    if initial_state is None:
        # Create initial state
        initial_state = {
            "messages": [AIMessage(content=SYSTEM_PROMPT)],
            "user_query": user_query,
            "dataset_loaded": False,
            "dataset_info": None,
            "execution_history": [],
            "current_step": "start"
        }
    else:
        # Add the new user query
        initial_state["user_query"] = user_query
        initial_state["messages"].append(HumanMessage(content=user_query))
    
    # Run the agent
    result = app.invoke(initial_state)
    
    # Update state with results
    result["dataset_loaded"] = dataset_tools.current_dataset is not None
    result["dataset_info"] = dataset_tools.dataset_info if dataset_tools.current_dataset is not None else None
    result["execution_history"] = dataset_tools.get_execution_history()
    result["current_step"] = "completed"
    
    return result

def create_studio_app() -> StateGraph:
    """
    Create a LangGraph Studio-compatible app.
    This provides the same functionality but with state management.
    """
    return app

if __name__ == "__main__":
    # Test the agent
    test_query = "Load the iris dataset and show me a correlation heatmap"
    result = run_agent(test_query)
    
    print("Agent Response:")
    for message in result["final_messages"]:
        if isinstance(message, AIMessage):
            print(f"AI: {message.content}")
        elif hasattr(message, 'content'):
            print(f"Tool: {message.content[:200]}...") 