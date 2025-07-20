#!/usr/bin/env python3
"""
LangChain Agent Chat UI Integration
Provides a ChatGPT-like interface for the Data Analysis AI Agent
"""

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agent.data_analysis_agent import app, SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, MessagesState
from langchain_openai import ChatOpenAI
import config

class ConversationSummarizer:
    """
    Handles conversation summarization to manage token usage
    """
    def __init__(self):
        self.summarizer_llm = ChatOpenAI(
            model=config.MODEL_NAME,
            temperature=0.1,
            api_key=config.OPENAI_API_KEY
        )
    
    def should_summarize(self, messages, max_messages=8):
        """Check if conversation should be summarized"""
        return len(messages) > max_messages
    
    def summarize_conversation(self, messages):
        """Summarize the conversation history"""
        if len(messages) <= 2:  # Just system message and current query
            return messages
        
        # Extract conversation exchanges (excluding system message)
        exchanges = []
        for i in range(1, len(messages) - 1, 2):  # Skip system message, process in pairs
            if i + 1 < len(messages):
                user_msg = messages[i].content if hasattr(messages[i], 'content') else str(messages[i])
                ai_msg = messages[i + 1].content if hasattr(messages[i + 1], 'content') else str(messages[i + 1])
                exchanges.append(f"User: {user_msg}\nAssistant: {ai_msg}")
        
        if not exchanges:
            return messages
        
        # Create summary prompt
        summary_prompt = f"""Summarize the following data analysis conversation exchanges. 
Focus on the key actions taken, datasets loaded, analyses performed, and important findings.
Keep the summary concise but informative.

Conversation exchanges:
{chr(10).join(exchanges)}

Summary:"""
        
        try:
            # Generate summary
            summary_response = self.summarizer_llm.invoke([HumanMessage(content=summary_prompt)])
            summary = summary_response.content
            
            # Create new message list with system message, summary, and current query
            current_query = messages[-1] if messages else None
            
            new_messages = [
                messages[0],  # System message
                AIMessage(content=f"Previous conversation summary: {summary}")
            ]
            
            if current_query:
                new_messages.append(current_query)
            
            return new_messages
            
        except Exception as e:
            print(f"Warning: Failed to summarize conversation: {e}")
            # Fallback: keep only system message and current query
            return [messages[0], messages[-1]] if len(messages) > 1 else messages

class AgentChatUIWrapper:
    """
    Wrapper for the agent that provides a clean interface for Agent Chat UI
    with conversation summarization
    """
    def __init__(self, app):
        self.app = app
        self.summarizer = ConversationSummarizer()
    
    def invoke(self, state):
        """
        Invoke the app with conversation summarization to manage token usage
        """
        messages = state.get("messages", [])
        
        # Check if we need to summarize
        if self.summarizer.should_summarize(messages):
            print("📝 Summarizing conversation to manage token usage...")
            messages = self.summarizer.summarize_conversation(messages)
            state["messages"] = messages
        
        # Call the original app
        result = self.app.invoke(state)
        
        return result

# Export the wrapped app for Agent Chat UI
# The Agent Chat UI expects a LangGraph app with a 'messages' key in the state
agent_chat_app = AgentChatUIWrapper(app)

# For testing the Agent Chat UI integration
if __name__ == "__main__":
    # Test the app with a sample query
    test_state = {
        "messages": [
            AIMessage(content=SYSTEM_PROMPT),
            HumanMessage(content="Load the iris dataset and show me basic statistics")
        ]
    }
    
    result = agent_chat_app.invoke(test_state)
    print("✅ Agent Chat UI integration test completed!")
    print(f"Final messages: {len(result['messages'])}")
    
    # Show the last AI response
    for message in reversed(result['messages']):
        if isinstance(message, AIMessage):
            print(f"AI Response: {message.content[:200]}...")
            break 