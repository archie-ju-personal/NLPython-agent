#!/usr/bin/env python3
"""
LangGraph app for data analysis agent - Studio Compatible Version
Uses the unified agent from agent/data_analysis_agent.py
"""

import json
from typing import Dict, Any, List, Optional, Annotated
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langgraph.graph import StateGraph, END
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agent.data_analysis_agent import app, AgentState, SYSTEM_PROMPT

# Export app for LangGraph Studio
app = app

# For LangGraph Studio compatibility
if __name__ == "__main__":
    # Test the app
    test_state = {
        "messages": [
            AIMessage(content=SYSTEM_PROMPT)
        ],
        "user_query": "can you please load the dataset iris, then Create a scatter plot of sepal length vs sepal width",
        "dataset_loaded": False,
        "dataset_info": None,
        "execution_history": [],
        "current_step": "start"
    }
    
    result = app.invoke(test_state)
    print("Test completed successfully!")
    print(f"Final messages: {len(result['messages'])}") 