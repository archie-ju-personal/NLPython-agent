#!/usr/bin/env python3
"""
Simple test script for the Data Analysis AI Agent
"""

import json
from agent.data_analysis_agent import run_agent
from tools.dataset_tools import dataset_tools

def test_basic_functionality():
    """Test basic agent functionality."""
    print("🧪 Testing Data Analysis AI Agent...")
    
    # Test 1: Load dataset
    print("\n1. Testing dataset loading...")
    result = dataset_tools.load_iris_dataset()
    if result['success']:
        print("✅ Dataset loaded successfully")
        print(f"   Shape: {result['info']['shape']}")
        print(f"   Columns: {', '.join(result['info']['columns'])}")
    else:
        print(f"❌ Dataset loading failed: {result['message']}")
        return False
    
    # Test 2: Get dataset info
    print("\n2. Testing dataset info retrieval...")
    info_result = dataset_tools.get_dataset_info()
    if info_result['success']:
        print("✅ Dataset info retrieved successfully")
    else:
        print(f"❌ Dataset info failed: {info_result['message']}")
        return False
    
    # Test 3: Execute simple code
    print("\n3. Testing code execution...")
    code_result = dataset_tools.execute_python_code("print('Dataset shape:', df.shape)\nprint('Columns:', list(df.columns))")
    if code_result['success']:
        print("✅ Code execution successful")
        print(f"   Output: {code_result['output'][:100]}...")
    else:
        print(f"❌ Code execution failed: {code_result['message']}")
        return False
    
    # Test 4: Create visualization
    print("\n4. Testing visualization creation...")
    viz_result = dataset_tools.create_visualization("correlation_heatmap")
    if viz_result['success']:
        print("✅ Visualization created successfully")
    else:
        print(f"❌ Visualization failed: {viz_result['message']}")
        return False
    
    # Test 5: Agent workflow
    print("\n5. Testing agent workflow...")
    agent_result = run_agent("Load the iris dataset and show me the first 3 rows")
    if agent_result and 'final_messages' in agent_result:
        print("✅ Agent workflow successful")
        # Find the final AI response
        for message in agent_result['final_messages']:
            if hasattr(message, 'content') and message.content:
                if not ("AI:" in str(message.content) or "Tool:" in str(message.content)):
                    print(f"   Response: {message.content[:100]}...")
                    break
    else:
        print("❌ Agent workflow failed")
        return False
    
    print("\n🎉 All tests passed! The agent is working correctly.")
    return True

def test_natural_language_queries():
    """Test various natural language queries."""
    print("\n🔍 Testing Natural Language Queries...")
    
    test_queries = [
        "Load the iris dataset",
        "Show me basic statistics of the dataset",
        "Create a correlation heatmap",
        "What are the column names in the dataset?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        try:
            result = run_agent(query)
            if result and 'final_messages' in result:
                print("   ✅ Query processed successfully")
                # Find the final AI response
                for message in result['final_messages']:
                    if hasattr(message, 'content') and message.content:
                        if not ("AI:" in str(message.content) or "Tool:" in str(message.content)):
                            print(f"   Response: {message.content[:80]}...")
                            break
            else:
                print("   ❌ Query failed")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Data Analysis AI Agent Tests...")
    
    # Run basic functionality tests
    if test_basic_functionality():
        # Run natural language query tests
        test_natural_language_queries()
        
        print("\n📊 Test Summary:")
        print("✅ Basic functionality tests passed")
        print("✅ Natural language query tests completed")
        print("\n🎯 The agent is ready to use!")
        print("\nNext steps:")
        print("1. Run 'python cli.py chat' for interactive mode")
        print("2. Run 'python cli.py demo' for a full demonstration")
        print("3. Run 'langgraph dev langgraph_studio.py' for LangGraph Studio")
    else:
        print("\n❌ Tests failed. Please check the configuration and dependencies.") 