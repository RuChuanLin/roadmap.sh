import argparse
import json
import os
from datetime import datetime

# File to store tasks
TASKS_FILE = "tasks.json"

def initialize_file():
    """Ensure the tasks file exists."""
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as file:
            json.dump([], file)

def add_task(description):
    """Add a new task to the list."""
    initialize_file()
    with open(TASKS_FILE, "r") as file:
        tasks = json.load(file)
    
    task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }
    tasks.append(task)
    
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)
    print(f"Task added: {task['id']} - {task['description']}")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument("command", choices=["add", "list", "update", "delete"], help="Command to execute")
    parser.add_argument("description", nargs="?", help="Task description for 'add' command")
    args = parser.parse_args()

    if args.command == "add" and args.description:
        add_task(args.description)
    elif args.command == "list":
        print("Listing tasks...")
        # To implement
    else:
        print("Invalid command or missing arguments.")

if __name__ == "__main__":
    main()
