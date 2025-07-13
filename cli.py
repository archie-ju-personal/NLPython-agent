#!/usr/bin/env python3
"""
CLI interface for the Data Analysis AI Agent
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
import json
from agent.data_analysis_agent import run_agent
from tools.dataset_tools import dataset_tools

app = typer.Typer()
console = Console()

@app.command()
def chat():
    """Start an interactive chat session with the AI agent."""
    console.print(Panel.fit(
        "[bold blue]Data Analysis AI Agent[/bold blue]\n"
        "Ask me to analyze datasets using natural language!",
        border_style="blue"
    ))
    
    console.print("\n[green]Available commands:[/green]")
    console.print("• 'quit' or 'exit' - End the session")
    console.print("• 'history' - Show execution history")
    console.print("• 'info' - Show current dataset info")
    console.print("• 'reset' - Reset to original dataset")
    console.print("• 'help' - Show this help")
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            elif user_input.lower() == 'history':
                history = dataset_tools.get_execution_history()
                if history:
                    table = Table(title="Execution History")
                    table.add_column("Timestamp", style="cyan")
                    table.add_column("Code", style="green")
                    table.add_column("Output", style="yellow")
                    
                    for entry in history[-5:]:  # Show last 5 entries
                        timestamp = entry['timestamp'].strftime("%H:%M:%S")
                        code = entry['code'][:50] + "..." if len(entry['code']) > 50 else entry['code']
                        output = entry['output'][:50] + "..." if len(entry['output']) > 50 else entry['output']
                        table.add_row(timestamp, code, output)
                    
                    console.print(table)
                else:
                    console.print("[yellow]No execution history yet.[/yellow]")
                continue
            elif user_input.lower() == 'info':
                info = dataset_tools.get_dataset_info()
                if info['success']:
                    console.print(Panel(
                        f"[bold]Dataset Info:[/bold]\n"
                        f"Shape: {info['info']['shape']}\n"
                        f"Columns: {', '.join(info['info']['columns'])}\n"
                        f"Missing values: {info['info']['missing_values']}",
                        title="Dataset Information",
                        border_style="green"
                    ))
                else:
                    console.print(f"[red]{info['message']}[/red]")
                continue
            elif user_input.lower() == 'reset':
                result = dataset_tools.reset_dataset()
                if result['success']:
                    console.print("[green]Dataset reset successfully![/green]")
                else:
                    console.print(f"[red]{result['message']}[/red]")
                continue
            elif user_input.lower() == 'help':
                console.print("\n[green]Available commands:[/green]")
                console.print("• 'quit' or 'exit' - End the session")
                console.print("• 'history' - Show execution history")
                console.print("• 'info' - Show current dataset info")
                console.print("• 'reset' - Reset to original dataset")
                console.print("• 'help' - Show this help")
                console.print("\n[green]Example queries:[/green]")
                console.print("• 'Load the iris dataset and show me basic statistics'")
                console.print("• 'Create a correlation heatmap'")
                console.print("• 'Show me a scatter plot of sepal length vs sepal width'")
                console.print("• 'Train a logistic regression model to predict species'")
                continue
            
            # Run the agent
            console.print("\n[bold blue]AI Agent[/bold blue] is thinking...")
            result = run_agent(user_input)
            
            # Display the response
            for message in result["final_messages"]:
                if hasattr(message, 'content') and message.content:
                    if "AI:" in str(message.content) or "Tool:" in str(message.content):
                        # Skip tool messages in CLI display
                        continue
                    else:
                        console.print(Panel(
                            message.content,
                            title="AI Response",
                            border_style="blue"
                        ))
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

@app.command()
def test():
    """Run a quick test of the agent with a sample query."""
    console.print("[bold blue]Testing the AI Agent...[/bold blue]")
    
    test_queries = [
        "Load the iris dataset and show me basic information",
        "Create a correlation heatmap",
        "Show me the first 5 rows of the dataset"
    ]
    
    for i, query in enumerate(test_queries, 1):
        console.print(f"\n[bold cyan]Test {i}:[/bold cyan] {query}")
        result = run_agent(query)
        
        # Show the final AI response
        for message in result["final_messages"]:
            if hasattr(message, 'content') and message.content:
                if not ("AI:" in str(message.content) or "Tool:" in str(message.content)):
                    console.print(f"[green]Response:[/green] {message.content[:200]}...")
                    break
    
    console.print("\n[bold green]Test completed![/bold green]")

@app.command()
def demo():
    """Run a demonstration of the agent's capabilities."""
    console.print(Panel.fit(
        "[bold blue]Data Analysis AI Agent Demo[/bold blue]\n"
        "This will demonstrate the agent's capabilities with the Iris dataset.",
        border_style="blue"
    ))
    
    demo_queries = [
        "Load the iris dataset",
        "Show me basic statistics and information about the dataset",
        "Create a correlation heatmap to see relationships between features",
        "Show me a scatter plot of sepal length vs sepal width, colored by species",
        "Train a logistic regression model to predict species and show the accuracy"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        console.print(f"\n[bold cyan]Step {i}:[/bold cyan] {query}")
        console.print("[dim]Processing...[/dim]")
        
        result = run_agent(query)
        
        # Show the final AI response
        for message in result["final_messages"]:
            if hasattr(message, 'content') and message.content:
                if not ("AI:" in str(message.content) or "Tool:" in str(message.content)):
                    console.print(Panel(
                        message.content,
                        title=f"Step {i} Response",
                        border_style="green"
                    ))
                    break
        
        if i < len(demo_queries):
            input("\nPress Enter to continue to the next step...")
    
    console.print("\n[bold green]Demo completed![/bold green]")

if __name__ == "__main__":
    app() 