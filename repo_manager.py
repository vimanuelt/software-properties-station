#!/usr/bin/env python3.11

import sys
import os
import logging
import config
import ui

CONFIG_FILE = '/etc/pkg/GhostBSD.conf'

# Set up logging
LOG_FILE = os.path.expanduser('~/software-properties-station.log')
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Check if running as root
if os.geteuid() != 0:
    sys.exit("This script must be run as root. Please use 'sudo' or log in as root.")

REPOS = config.load_repos()
logging.debug("Loaded repositories: %s", REPOS)

def update_config(repo_name):
    latest_url, base_url = REPOS[repo_name]
    config_content = (
        f'{repo_name}: {{\n'
        f'  url: "{latest_url}",\n'
        f'  signature_type: "pubkey",\n'
        f'  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",\n'
        f'  enabled: yes\n'
        f'}}\n'
        f'{repo_name}-base: {{\n'
        f'  url: "{base_url}",\n'
        f'  signature_type: "pubkey",\n'
        f'  pubkey: "/usr/share/keys/ssl/certs/ghostbsd.cert",\n'
        f'  enabled: yes\n'
        f'}}\n'
    )
    try:
        with open(CONFIG_FILE, 'w') as f:
            f.write(config_content)
        logging.info(f"Configuration updated with repository {repo_name}.")
    except Exception as e:
        logging.error(f"Error updating configuration: {e}")
        raise

def validate_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            config_content = f.read()
        if "url:" not in config_content:
            raise ValueError("Invalid configuration: missing URL.")
        logging.info("Configuration file validated.")
    except Exception as e:
        logging.error(f"Configuration validation failed: {e}")
        raise

def select_repo(repo_name):
    try:
        logging.debug("Selecting repository: %s", repo_name)
        update_config(repo_name)
        validate_config()
        return True, f'{repo_name} selected and configuration updated.'
    except Exception as e:
        logging.error(f"Error selecting repository: {e}")
        return False, str(e)

def list_repos():
    print("Available repositories:")
    for repo in REPOS.keys():
        print(f"  - {repo}")

def show_current_repo():
    try:
        with open(CONFIG_FILE, 'r') as f:
            config_content = f.read()
        for repo_name in REPOS.keys():
            if f'{repo_name}:' in config_content:
                print(f"Current repository: {repo_name}")
                return
        print("No known repository currently configured.")
    except Exception as e:
        logging.error(f"Error reading current configuration: {e}")
        print("Error reading current configuration.")

def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == '--list':
            list_repos()
            sys.exit(0)
        elif sys.argv[1] == '--current':
            show_current_repo()
            sys.exit(0)
        else:
            repo_name = sys.argv[1]
            if repo_name not in REPOS:
                print(f"Error: Repository '{repo_name}' not found.")
                sys.exit(1)
            success, message = select_repo(repo_name)
            print(message)
            sys.exit(0 if success else 1)
    else:
        ui.start_gui()

if __name__ == "__main__":
    main()
