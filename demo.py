#!/usr/bin/env python3
"""
Demo script for the Data Analysis AI Agent
"""

from agent.data_analysis_agent import run_agent
from langchain_core.messages import AIMessage
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import time

console = Console()

def demo_agent():
    """Demonstrate the AI agent's capabilities."""
    
    console.print(Panel.fit(
        "[bold blue]Data Analysis AI Agent Demo[/bold blue]\n"
        "Watch the agent translate natural language to executable Python code!",
        border_style="blue"
    ))
    
    # Demo queries
    demo_queries = [
        "Load the iris dataset and show me basic information about it",
        "Create a correlation heatmap to see relationships between features",
        "Show me the first 5 rows of the dataset",
        "Calculate the mean and standard deviation of all numeric columns",
        "Train a logistic regression model to predict species and show the accuracy"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        console.print(f"\n[bold cyan]Demo {i}:[/bold cyan] {query}")
        console.print("[dim]Processing...[/dim]")
        
        try:
            # Run the agent
            result = run_agent(query)
            
            # Display the final AI response
            for message in result["final_messages"]:
                if isinstance(message, AIMessage) and message.content:
                    # Skip system prompt messages
                    if "You are a data analysis AI agent" not in message.content:
                        console.print(Panel(
                            message.content,
                            title=f"AI Response {i}",
                            border_style="green"
                        ))
                        break
            
            time.sleep(1)  # Brief pause between demos
            
        except Exception as e:
            console.print(f"[red]Error in demo {i}: {str(e)}[/red]")
    
    console.print("\n[bold green]Demo completed![/bold green]")
    console.print("\n[bold]Next steps:[/bold]")
    console.print("• Run 'python cli.py chat' for interactive mode")
    console.print("• Run 'langgraph dev langgraph_studio.py' for LangGraph Studio")
    console.print("• Try your own natural language queries!")

if __name__ == "__main__":
    demo_agent() 