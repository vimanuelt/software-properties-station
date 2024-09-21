#!/usr/bin/env python3
# File: software_properties_station/main.py

import sys
import os

# Add the directories where config, repo, and ui modules are located
sys.path.append('/usr/share/software-properties-station')

from config.config import load_repos  # Import from config module
from repo.ghostbsd_repo_manager import update_config, list_repos  # Import repository management
from ui.ui import start_gui  # Import the GUI start function

def main():
    if len(sys.argv) > 1:
        # Check if the user passed --gui as an argument
        if sys.argv[1] == '--gui':
            # Start in GUI mode
            print("Starting in GUI mode...")
            gui_mode()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print_usage()
    else:
        # Default to CLI mode
        cli_mode()

def cli_mode():
    """
    Run the CLI interface to manage repositories.
    """
    repos = list_repos()
    if repos:
        print("Available repositories:")
        for repo in repos:
            print(f"- {repo}")

        selected_repo = input("Select a repository: ")
        success, message = update_config(selected_repo)
        if success:
            print(f"Repository '{selected_repo}' selected successfully.")
        else:
            print(f"Error: {message}")
    else:
        print("No repositories found.")

def gui_mode():
    """
    Start the GUI interface.
    """
    start_gui()

def print_usage():
    """
    Print usage information for the software-properties-station.
    """
    print("Usage:")
    print("  sudo software-properties-station            # Start in CLI mode (default)")
    print("  sudo software-properties-station --gui      # Start in GUI mode")

if __name__ == "__main__":
    main()

