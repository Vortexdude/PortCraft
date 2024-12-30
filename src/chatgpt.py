import os
import time
import subprocess
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import threading

console = Console()


# Function to clone a Git repository
def clone_repo(repo_url, dest_dir):
    console.print(f"[cyan]Cloning repository: {repo_url}[/cyan]")
    with Progress(
            SpinnerColumn(), BarColumn(), TextColumn("[progress.description]{task.description}")
    ) as progress:
        task = progress.add_task("Cloning...", total=None)
        try:
            subprocess.run(["git", "clone", repo_url, dest_dir], check=True)
            progress.update(task, completed=True)
            console.print(f"[green]Repository cloned successfully into {dest_dir}![/green]")
        except subprocess.CalledProcessError as e:
            progress.stop()
            console.print(f"[red]Failed to clone repository: {e}[/red]")


# Function to set environment variables
def set_variables():
    console.print("[cyan]Setting up environment variables...[/cyan]")
    os.environ["MY_VAR"] = "example_value"
    console.print("[green]Environment variables set successfully![/green]")


# Listener function to simulate event listening and execute a bash command
def event_listener(interval, bash_command):
    console.print(f"[yellow]Listening for events every {interval} seconds...[/yellow]")
    while True:
        time.sleep(interval)
        console.print("[blue]Event detected! Executing bash command...[/blue]")
        try:
            result = subprocess.run(bash_command, shell=True, capture_output=True, text=True)
            console.print(f"[green]Command Output:[/green] {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Command failed:[/red] {e}")


# Main function to orchestrate the tasks
def main():
    # Get user input using Rich prompt
    repo_url = Prompt.ask("[bold cyan]Enter the repository URL[/bold cyan]")
    dest_dir = Prompt.ask("[bold cyan]Enter the destination directory[/bold cyan]", default="./cloned_repo")
    bash_command = Prompt.ask("[bold cyan]Enter the bash command to execute on event[/bold cyan]",
                              default="echo 'Hello, World!'")

    # Clone the repository
    clone_repo(repo_url, dest_dir)

    # Set environment variables
    set_variables()

    # Start the event listener in a separate thread
    listener_thread = threading.Thread(target=event_listener, args=(5, bash_command), daemon=True)
    listener_thread.start()

    # Keep the main thread alive
    console.print("[bold green]Press Ctrl+C to exit the program.[/bold green]")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("[red]Exiting program...[/red]")


if __name__ == "__main__":
    main()