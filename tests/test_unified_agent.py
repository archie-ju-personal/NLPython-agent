#!/usr/bin/env python3
"""
Test script for the unified data analysis agent
Tests both CLI and Studio interfaces
"""

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agent.data_analysis_agent import run_agent, run_agent_with_state, app, AgentState, SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, AIMessage

def test_cli_interface():
    """Test the CLI interface (backward compatibility)"""
    print("🧪 Testing CLI Interface...")
    print("=" * 50)
    
    test_query = "Load the iris dataset and show me basic statistics"
    
    try:
        result = run_agent(test_query)
        
        print(f"✅ CLI interface test passed!")
        print(f"Query: {result['user_query']}")
        print(f"Messages returned: {len(result['final_messages'])}")
        
        # Show the last AI message
        for message in reversed(result['final_messages']):
            if isinstance(message, AIMessage):
                print(f"AI Response: {message.content[:200]}...")
                break
                
    except Exception as e:
        print(f"❌ CLI interface test failed: {e}")
        import traceback
        traceback.print_exc()

def test_studio_interface():
    """Test the Studio interface with state management"""
    print("\n🧪 Testing Studio Interface...")
    print("=" * 50)
    
    test_query = "Create a scatter plot of sepal length vs sepal width"
    
    try:
        result = run_agent_with_state(test_query)
        
        print(f"✅ Studio interface test passed!")
        print(f"Dataset loaded: {result.get('dataset_loaded', 'N/A')}")
        print(f"Current step: {result.get('current_step', 'N/A')}")
        print(f"Messages: {len(result.get('messages', []))}")
        print(f"Execution history entries: {len(result.get('execution_history', []))}")
        
        # Show the last AI message
        for message in reversed(result['messages']):
            if isinstance(message, AIMessage):
                print(f"AI Response: {message.content[:200]}...")
                break
                
    except Exception as e:
        print(f"❌ Studio interface test failed: {e}")
        import traceback
        traceback.print_exc()

def test_langgraph_app():
    """Test the LangGraph app directly"""
    print("\n🧪 Testing LangGraph App...")
    print("=" * 50)
    
    test_state = {
        "messages": [AIMessage(content=SYSTEM_PROMPT)],
        "user_query": "Load the iris dataset and get dataset info",
        "dataset_loaded": False,
        "dataset_info": None,
        "execution_history": [],
        "current_step": "start"
    }
    
    try:
        result = app.invoke(test_state)
        
        print(f"✅ LangGraph app test passed!")
        print(f"Final messages: {len(result['messages'])}")
        print(f"State keys: {list(result.keys())}")
        
    except Exception as e:
        print(f"❌ LangGraph app test failed: {e}")
        import traceback
        traceback.print_exc()

def test_state_persistence():
    """Test that state is properly maintained across calls"""
    print("\n🧪 Testing State Persistence...")
    print("=" * 50)
    
    queries = [
        "Load the iris dataset",
        "Show me basic statistics",
        "Create a correlation heatmap"
    ]
    
    try:
        state = None
        for i, query in enumerate(queries, 1):
            print(f"Step {i}: {query}")
            state = run_agent_with_state(query, state)
            print(f"  Dataset loaded: {state['dataset_loaded']}")
            print(f"  Execution history: {len(state['execution_history'])} entries")
        
        print(f"✅ State persistence test passed!")
        print(f"Final state - Dataset loaded: {state['dataset_loaded']}")
        print(f"Final state - Execution history: {len(state['execution_history'])} entries")
        
    except Exception as e:
        print(f"❌ State persistence test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all tests"""
    print("🚀 Testing Unified Data Analysis Agent")
    print("=" * 60)
    
    # Test all interfaces
    test_cli_interface()
    test_studio_interface()
    test_langgraph_app()
    test_state_persistence()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main() 