#!/usr/bin/env python3
"""
Test script for conversation summarization
Tests the token management feature for Agent Chat UI
"""

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from interfaces.agent_chat_ui import agent_chat_app, ConversationSummarizer
from agent.data_analysis_agent import SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, AIMessage

def test_conversation_summarizer():
    """Test the conversation summarizer functionality"""
    print("🧪 Testing Conversation Summarizer...")
    print("=" * 60)
    
    summarizer = ConversationSummarizer()
    
    # Test 1: Short conversation (should not summarize)
    short_messages = [
        AIMessage(content=SYSTEM_PROMPT),
        HumanMessage(content="Hello"),
        AIMessage(content="Hi there!")
    ]
    
    should_summarize = summarizer.should_summarize(short_messages)
    print(f"Short conversation ({len(short_messages)} messages): Should summarize = {should_summarize}")
    
    # Test 2: Long conversation (should summarize)
    long_messages = [
        AIMessage(content=SYSTEM_PROMPT),
        HumanMessage(content="Load the iris dataset"),
        AIMessage(content="Dataset loaded successfully"),
        HumanMessage(content="Show me basic statistics"),
        AIMessage(content="Here are the statistics..."),
        HumanMessage(content="Create a scatter plot"),
        AIMessage(content="Plot created successfully"),
        HumanMessage(content="Show correlation"),
        AIMessage(content="Correlation matrix shown"),
        HumanMessage(content="Train a model"),
        AIMessage(content="Model trained successfully")
    ]
    
    should_summarize = summarizer.should_summarize(long_messages)
    print(f"Long conversation ({len(long_messages)} messages): Should summarize = {should_summarize}")
    
    if should_summarize:
        print("📝 Testing summarization...")
        summarized = summarizer.summarize_conversation(long_messages)
        print(f"Original messages: {len(long_messages)}")
        print(f"Summarized messages: {len(summarized)}")
        
        # Show the summary
        for message in summarized:
            if isinstance(message, AIMessage) and "Previous conversation summary" in message.content:
                print(f"Summary: {message.content[:200]}...")
                break

def test_agent_chat_with_summarization():
    """Test the agent chat with summarization enabled"""
    print("\n🧪 Testing Agent Chat with Summarization...")
    print("=" * 60)
    
    # Create a conversation that would trigger summarization
    test_queries = [
        "Load the iris dataset",
        "Show me basic statistics",
        "Create a scatter plot of sepal length vs sepal width",
        "Show correlation between all features",
        "Train a logistic regression model"
    ]
    
    messages = [AIMessage(content=SYSTEM_PROMPT)]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[bold cyan]Query {i}:[/bold cyan] {query}")
        
        # Add the user query
        messages.append(HumanMessage(content=query))
        
        try:
            # Test the agent with current conversation
            test_state = {"messages": messages}
            result = agent_chat_app.invoke(test_state)
            
            print(f"✅ Query {i} completed!")
            print(f"Messages after processing: {len(result['messages'])}")
            
            # Update messages for next iteration
            messages = result['messages']
            
            # Check if summarization occurred
            if len(messages) < len(test_state["messages"]):
                print("📝 Summarization was applied!")
            
        except Exception as e:
            print(f"❌ Query {i} failed: {e}")
            import traceback
            traceback.print_exc()

def test_token_usage_reduction():
    """Test that summarization reduces token usage"""
    print("\n🧪 Testing Token Usage Reduction...")
    print("=" * 60)
    
    # Create a conversation with many exchanges
    messages = [AIMessage(content=SYSTEM_PROMPT)]
    
    # Add multiple exchanges to simulate a long conversation
    for i in range(10):
        messages.append(HumanMessage(content=f"Query {i+1}: Load dataset and show statistics"))
        messages.append(AIMessage(content=f"Response {i+1}: Dataset loaded with detailed statistics including mean, std, min, max for all numeric columns. The dataset contains 150 samples with 4 features."))
    
    print(f"Original conversation length: {len(messages)} messages")
    
    # Estimate token usage (rough approximation)
    total_chars = sum(len(str(msg.content)) for msg in messages)
    estimated_tokens = total_chars // 4  # Rough estimate: 1 token ≈ 4 characters
    print(f"Estimated original tokens: {estimated_tokens:,}")
    
    # Apply summarization
    summarizer = ConversationSummarizer()
    if summarizer.should_summarize(messages):
        summarized = summarizer.summarize_conversation(messages)
        
        total_chars_summarized = sum(len(str(msg.content)) for msg in summarized)
        estimated_tokens_summarized = total_chars_summarized // 4
        
        print(f"Summarized conversation length: {len(summarized)} messages")
        print(f"Estimated summarized tokens: {estimated_tokens_summarized:,}")
        print(f"Token reduction: {estimated_tokens - estimated_tokens_summarized:,} tokens ({((estimated_tokens - estimated_tokens_summarized) / estimated_tokens * 100):.1f}%)")

def main():
    """Run all conversation summarization tests"""
    print("🚀 Testing Conversation Summarization")
    print("=" * 60)
    
    # Test all aspects
    test_conversation_summarizer()
    test_agent_chat_with_summarization()
    test_token_usage_reduction()
    
    print("\n🎉 All conversation summarization tests completed!")

if __name__ == "__main__":
    main() 