# Software Properties Station Architecture

## Overview

The software-properties-station app is a graphical and command-line application designed to help users of GhostBSD manage their package repositories. It is built using Python 3.11 and GTK 3.0 for the graphical interface. The application is divided into several modules, each responsible for different aspects of its functionality.

## Modules

### config.py

This module is responsible for loading the repository configurations. It defines the available repositories and their URLs.

```
def load_repos():
    repos = {
        "GhostBSD_Unstable": ("http://pkg.ghostbsd.org/unstable/${ABI}/latest", "http://pkg.ghostbsd.org/unstable/${ABI}/base"),
        "GhostBSD_CA": ("https://pkg.ca.ghostbsd.org/stable/${ABI}/latest", "https://pkg.ca.ghostbsd.org/stable/${ABI}/base"),
        "GhostBSD": ("https://pkg.ghostbsd.org/stable/${ABI}/latest", "https://pkg.ghostbsd.org/stable/${ABI}/base"),
        "GhostBSD_FR": ("https://pkg.fr.ghostbsd.org/stable/${ABI}/latest", "https://pkg.fr.ghostbsd.org/stable/${ABI}/base"),
        "GhostBSD_NO": ("http://pkg.no.ghostbsd.org/stable/${ABI}/latest", "http://pkg.no.ghostbsd.org/stable/${ABI}/base"),
        "GhostBSD_ZA": ("https://pkg.za.ghostbsd.org/stable/${ABI}/latest", "https://pkg.za.ghostbsd.org/stable/${ABI}/base")
    }
    return repos
```

### repo_manager.py

This module handles the core functionality of selecting, updating, and validating the repository configuration.

- **update_config(repo_name)**: Updates the configuration file with the selected repository URLs.
- **validate_config()**: Validates the configuration file to ensure it contains the necessary URLs.
- **select_repo(repo_name)**: Orchestrates the update and validation process.
- **list_repos()**: Lists all available repositories.
- **show_current_repo()**: Shows the currently configured repository.

```
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
```

### ui.py

This module defines the graphical interface using GTK 3.0. It provides a window with buttons for each repository and handles user interactions.

- **RepoSelector**: Main window class.
- **on_repo_selected()**: Handles repository selection events.
- **update_repository(repo_name)**: Updates the repository configuration and displays status messages.
- **show_message(title, message)**: Displays information or error messages.
- **show_progress(message)**: Shows a progress dialog during operations.

```
class RepoSelector(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Software Properties Station")
        self.set_border_width(10)
        self.set_default_size(400, 300)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        title_label = Gtk.Label(label="Select Package Repository")
        vbox.pack_start(title_label, False, False, 0)

        if not repo_manager.REPOS:
            error_label = Gtk.Label(label="No repositories loaded. Please check the configuration.")
            vbox.pack_start(error_label, False, False, 0)
        else:
            for name in repo_manager.REPOS.keys():
                button = Gtk.Button(label=name)
                button.set_tooltip_text(f"Select the {name} repository")
                button.connect("clicked", self.on_repo_selected, name)
                vbox.pack_start(button, False, False, 0)

        quit_button = Gtk.Button(label="Quit")
        quit_button.set_tooltip_text("Quit the application")
        quit_button.connect("clicked", self.quit)
        vbox.pack_start(quit_button, False, False, 0)

        self.statusbar = Gtk.Statusbar()
        self.context_id = self.statusbar.get_context_id("status")
        vbox.pack_start(self.statusbar, False, False, 0)

    def on_repo_selected(self, widget, repo_name):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Confirm Repository Change",
        )
        dialog.format_secondary_text(f"Do you want to change the repository to {repo_name}?")
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            self.show_progress("Updating repository configuration...")
            GLib.idle_add(self.update_repository, repo_name)

    def update_repository(self, repo_name):
        success, message = repo_manager.select_repo(repo_name)
        self.statusbar.push(self.context_id, message)
        self.show_message("Success" if success else "Error", message)
        return False

    def show_message(self, title, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO if title == "Success" else Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def show_progress(self, message):
        progress_dialog = Gtk.Dialog(
            transient_for=self,
            flags=0,
            title="Progress"
        )
        progress_dialog.set_modal(True)
        progress_dialog.set_decorated(False)
        label = Gtk.Label(label=message)
        progress_dialog.get_content_area().pack_start(label, True, True, 0)
        spinner = Gtk.Spinner()
        spinner.start()
        progress_dialog.get_content_area().pack_start(spinner, True, True, 0)
        progress_dialog.show_all()
        GLib.timeout_add(1000, progress_dialog.destroy)

    def quit(self, widget):
        Gtk.main_quit()

def launch_gui():
    win = RepoSelector()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
```

### software-properties-station

This is the main script that handles both the command-line interface and the graphical interface. It checks if the script is run as root and then proceeds based on the provided command-line arguments or launches the GUI.

```
#!/usr/bin/env python3.11
import sys
from repo_manager import main

if __name__ == "__main__":
    main()
```

## Flow

1. **Initialization**: The GUI is launched, and the repositories are loaded from `config.py`.
2. **User Interaction**: The user selects a repository using the GUI or CLI.
3. **Update**: The selected repository URLs are written to the configuration file.
4. **Validation**: The configuration file is validated.
5. **Feedback**: The user is informed of the success or failure of the operation through status messages and dialogs (GUI) or console output (CLI).

## Error Handling

The application logs errors to `~/software-properties-statin.log` and provides user feedback through dialogs and the status bar (GUI) or console output (CLI). Exceptions are caught and logged, ensuring the application can provide useful error messages to the user.

## Future Improvements

- **Dynamic Repository Loading**: Allow repositories to be added or removed without modifying the source code.
- **Advanced Validation**: Enhance the validation process to check for more potential issues.
- **Localization**: Support multiple languages for the GUI.

