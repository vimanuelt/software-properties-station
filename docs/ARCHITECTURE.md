# Software Properties Station Architecture

## Overview

**Software Properties Station** is a dual-interface (GUI and CLI) application designed for GhostBSD users to manage package repositories. Built with Python 3.11 and GTK 4.0 for the GUI, it provides a seamless experience for repository management. The application's architecture is modular, facilitating maintenance and future enhancements.

## Modules

### `config.py`

- **Purpose**: Manages repository configurations.
- **Location**: `/config/`
- **Key Function**: `load_repos()` - Loads repository data into a dictionary for use across the application.

```python
def load_repos():
    return {
        "GhostBSD": ("url", "base_url"),
        "GhostBSD_Canada": ("url", "base_url"),
        # Additional repositories...
    }
```

### `ghostbsd_repo_manager.py`

- **Core Functionality**: Handles repository operations like selection, updating, and validation.
- **Location**: `/repo/`
- **Functions**:
  - `select_repo(repo_name)`: Updates the configuration file with the selected repository's details.
  - `update_config(repo_name)`: Orchestrates the repository selection process.
  - `validate_config()`: Ensures the configuration file meets necessary criteria.
  - `list_repos()`: Outputs available repositories.

```python
# Example structure for ghostbsd_repo_manager.py
def update_config(repo_name):
    # Updates repository configuration

def validate_config():
    # Validates repository configuration
```

### `ui.py`

- **GUI Implementation**: Uses GTK 4.0 to create an interactive interface.
- **Location**: `/ui/`
- **Key Components**:
  - **RepoSelector**: The main window class managing UI elements.
  - `on_repo_selected()`: Handles repository selection events.
  - `show_message()`: Manages UI feedback for operations.

```python
class RepoSelector(Gtk.Window):
    def __init__(self):
        # Initializes UI components

    def on_repo_selected(self, widget, repo_name):
        # Handle repository selection

    def show_message(self, message, message_type):
        # Display messages
```

### Main Script (`main.py`)

- **Purpose**: This is the entry point of the application.
- **Location**: `/software_properties_station/`
- **Functionality**:
  - Runs the CLI by default or the GUI when `--gui` is passed.
  - Manages user interactions for selecting repositories.

```python
#!/usr/bin/env python3
import sys
import config.config
import repo.ghostbsd_repo_manager as ghostbsd_repo_manager
import ui.ui as ui

def main():
    # Entry point for the software-properties-station
```

## Logs

- **Log Path**: Logs are written to `/var/log/software-properties-station/software-properties-station.log`.
- **Logging Setup**: Logs both errors and normal operation statuses.

```python
LOG_FILE = '/var/log/software-properties-station/software-properties-station.log'
```

## System Flow

1. **Initialization**: The application starts by loading repositories from `config.py`.
2. **User Interaction**: Users engage with the system either through GUI or CLI to select repositories.
3. **Repository Management**: The selected repository is updated in the configuration file.
4. **Validation**: The configuration is validated post-update.
5. **Feedback**: Users receive feedback on operations via the GUI's status messages or CLI output.

## Recent Enhancements

- **Filesystem Restructuring**: 
  - `/config/`: Contains configuration management (`config.py`).
  - `/repo/`: Manages repository operations (`ghostbsd_repo_manager.py`).
  - `/software_properties_station/`: Main script resides here.
  - `/ui/`: Manages the GUI components (`ui.py`).
  - `/docs/`: Contains documentation like `ARCHITECTURE.md`.
  - `/tests/`: Placeholder for unit tests.

- **Logging**: Moved log storage to `/var/log/software-properties-station/` for system-wide logging.
- **Module Search Path**: Updated the main script to include custom directories in the Python module search path.

## Development Guidelines

- **Code Style**: Adhere to PEP 8 for Python code style.
- **Version Control**: Use Git for version control with descriptive commit messages.
- **Testing**: Implement unit tests for core functionalities, especially in `ghostbsd_repo_manager.py`.
- **Documentation**: Maintain detailed documentation for each module and function.

## Deployment

- **Environment**: Ensure the application runs on GhostBSD with the required Python version and GTK libraries.
- **Installation**: Provide a straightforward installation script or package for GhostBSD users.

## Security Considerations

- **Repository Validation**: Ensure all repository URLs are validated against a whitelist to prevent unauthorized repository additions.
- **Permissions**: The application should run with root privileges only when necessary, minimizing security risks.

