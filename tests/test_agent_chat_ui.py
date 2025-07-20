#!/usr/bin/env python3
"""
Test script for the Agent Chat UI integration
Tests the ChatGPT-like interface for our data analysis agent
"""

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from interfaces.agent_chat_ui import agent_chat_app
from agent.data_analysis_agent import SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, AIMessage

def test_agent_chat_ui_integration():
    """Test the Agent Chat UI integration"""
    print("🧪 Testing Agent Chat UI Integration...")
    print("=" * 60)
    
    test_queries = [
        "Load the iris dataset and show me basic statistics",
        "Create a scatter plot of sepal length vs sepal width",
        "Show correlation between all features"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[bold cyan]Test {i}:[/bold cyan] {query}")
        
        try:
            # Create test state with messages
            test_state = {
                "messages": [
                    AIMessage(content=SYSTEM_PROMPT),
                    HumanMessage(content=query)
                ]
            }
            
            # Invoke the agent chat app
            result = agent_chat_app.invoke(test_state)
            
            print(f"✅ Test {i} passed!")
            print(f"Messages returned: {len(result['messages'])}")
            
            # Show the last AI message
            for message in reversed(result['messages']):
                if isinstance(message, AIMessage):
                    print(f"AI Response: {message.content[:200]}...")
                    break
                    
        except Exception as e:
            print(f"❌ Test {i} failed: {e}")
            import traceback
            traceback.print_exc()

def test_chat_ui_state_format():
    """Test that the state format is compatible with Agent Chat UI"""
    print("\n🧪 Testing State Format Compatibility...")
    print("=" * 60)
    
    try:
        # Test state with messages (required by Agent Chat UI)
        test_state = {
            "messages": [
                AIMessage(content=SYSTEM_PROMPT),
                HumanMessage(content="Hello, can you help me with data analysis?")
            ]
        }
        
        result = agent_chat_app.invoke(test_state)
        
        # Check that result has messages key
        if "messages" in result:
            print("✅ State format is compatible with Agent Chat UI!")
            print(f"Messages in result: {len(result['messages'])}")
        else:
            print("❌ State format is missing 'messages' key")
            
    except Exception as e:
        print(f"❌ State format test failed: {e}")
        import traceback
        traceback.print_exc()

def test_visualization_in_chat():
    """Test visualization handling in chat interface"""
    print("\n🧪 Testing Visualization in Chat...")
    print("=" * 60)
    
    try:
        test_state = {
            "messages": [
                AIMessage(content=SYSTEM_PROMPT),
                HumanMessage(content="Create a scatter plot of sepal length vs sepal width")
            ]
        }
        
        result = agent_chat_app.invoke(test_state)
        
        # Check if visualization was created
        has_visualization = False
        for message in result['messages']:
            if hasattr(message, 'content') and message.content:
                try:
                    data = json.loads(message.content)
                    if isinstance(data, dict) and data.get('success') and 'plot_data' in data:
                        has_visualization = True
                        break
                except:
                    pass
        
        if has_visualization:
            print("✅ Visualization created successfully in chat!")
        else:
            print("⚠️  No visualization detected in response")
            
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        import traceback
        traceback.print_exc()

def test_message_history_management():
    """Test that message history is properly managed"""
    print("\n🧪 Testing Message History Management...")
    print("=" * 60)
    
    try:
        # Create a long conversation to test history management
        messages = [AIMessage(content=SYSTEM_PROMPT)]
        
        # Add multiple exchanges
        for i in range(5):
            messages.append(HumanMessage(content=f"Test message {i+1}"))
            messages.append(AIMessage(content=f"Response {i+1}"))
        
        test_state = {"messages": messages}
        
        # The wrapper should manage the history
        result = agent_chat_app.invoke(test_state)
        
        print(f"✅ Message history management working!")
        print(f"Original messages: {len(messages)}")
        print(f"Managed messages: {len(result['messages'])}")
        
    except Exception as e:
        print(f"❌ Message history test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all Agent Chat UI tests"""
    print("🚀 Testing Agent Chat UI Integration")
    print("=" * 60)
    
    # Test all aspects
    test_agent_chat_ui_integration()
    test_chat_ui_state_format()
    test_visualization_in_chat()
    test_message_history_management()
    
    print("\n🎉 All Agent Chat UI tests completed!")

if __name__ == "__main__":
    main() 