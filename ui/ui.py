#!/usr/bin/env python3
# File: ui.py

import os
import gi

# Set the GTK version before importing Gtk
gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, Pango, GLib, Gdk, Gio
import logging

# Import the tabs
from ui.ghostbsd_repos_tab import GhostBSDReposTab  # Existing GhostBSD Repositories tab
from ui.custom_repos_tab import CustomReposTab      # New Custom Repositories tab
# from ui.status_tab import StatusTab                 # Existing Status tab

# Constants
TITLE = "Software Properties Station"
WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 480 
CONFIG_FILE = '/etc/pkg/GhostBSD.conf'
LOG_FILE = '/var/log/software-properties-station/software-properties-station.log'

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class RepoSelector(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title=TITLE)

        # CSS Provider to add margins or padding
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data("""
            window { padding: 10px; }
        """, -1)

        style_context = self.get_style_context()
        style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Header Bar (replaces toolbar)
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_title_buttons(True)

        # Create a label for the title and add it to the HeaderBar
        title_label = Gtk.Label(label=TITLE)
        header_bar.set_title_widget(title_label)

        self.set_titlebar(header_bar)

        # Main layout
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(main_vbox)

        # Notebook for tabs
        notebook = Gtk.Notebook()

        # GhostBSD Repositories tab
        ghostbsd_repos_tab = GhostBSDReposTab()  # Existing tab
        notebook.append_page(ghostbsd_repos_tab, Gtk.Label(label="GhostBSD Repositories"))

        # Custom Repositories tab (new, placeholder only)
        custom_repos_tab = CustomReposTab()  # New tab for managing custom repositories
        notebook.append_page(custom_repos_tab, Gtk.Label(label="Custom Repositories"))

        # Status tab
        # status_tab = StatusTab()  # Existing tab
        # notebook.append_page(status_tab, Gtk.Label(label="Status"))

        main_vbox.append(notebook)

        # Quit button
        quit_button = Gtk.Button(label="Quit")
        quit_button.connect("clicked", self.on_quit)

        # Create a box to hold the quit button
        button_box = Gtk.Box(spacing=6)
        button_box.set_halign(Gtk.Align.END)
        button_box.append(quit_button)

        main_vbox.append(button_box)

    def on_quit(self, widget):
        self.close()

class SoftwarePropertiesApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.gtk.example")

    def do_activate(self):
        # Create the main window
        win = RepoSelector(self)
        win.present()

def start_gui():
    app = SoftwarePropertiesApp()
    app.run(None)

if __name__ == "__main__":
    start_gui()

