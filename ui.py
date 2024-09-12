#!/usr/bin/env python3.11

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Pango, GLib
import repo_manager

class RepoSelector(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Software Properties Station")
        self.set_border_width(10)
        self.set_default_size(600, 400)
        
        # Create a main vertical box to hold all elements
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(main_vbox)

        # Add a toolbar for common actions
        toolbar = self.create_toolbar()
        main_vbox.pack_start(toolbar, False, False, 0)

        # Create a notebook for tabs
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        
        # First tab: Repository Selection
        repo_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.create_repo_tab(repo_vbox)
        notebook.append_page(repo_vbox, Gtk.Label(label="Repositories"))

        # Second tab: Status and Messages
        status_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.create_status_tab(status_vbox)
        notebook.append_page(status_vbox, Gtk.Label(label="Status"))

        main_vbox.pack_start(notebook, True, True, 0)

        # Add Quit button
        quit_button = Gtk.Button(label="Quit")
        quit_button.connect("clicked", self.on_quit)
        quit_button_box = Gtk.Box()
        quit_button_box.pack_end(quit_button, False, False, 0)
        main_vbox.pack_end(quit_button_box, False, False, 0)

        self.show_all()

    def create_toolbar(self):
        toolbar = Gtk.Toolbar()
#        refresh_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REFRESH)
#        refresh_button.connect("clicked", self.refresh_repos)
#        toolbar.insert(refresh_button, -1)
        return toolbar

    def create_repo_tab(self, vbox):
        # Add a label for instructions
        instruction_label = Gtk.Label(label="Select a package repository")
        instruction_label.set_alignment(0.0, 0.5)  # Left align the text
        instruction_label.set_hexpand(True)
        instruction_label.set_vexpand(False)
        vbox.pack_start(instruction_label, False, False, 0)  # Don't expand, just add space for the label

        repo_scrolled = Gtk.ScrolledWindow()
        repo_scrolled.set_hexpand(True)
        repo_scrolled.set_vexpand(True)
        vbox.pack_start(repo_scrolled, True, True, 0)

        repo_list = Gtk.ListBox()
        repo_list.set_selection_mode(Gtk.SelectionMode.NONE)
        repo_list.set_vexpand(True)
        repo_list.connect("row-activated", self.on_repo_selected)
        repo_scrolled.add(repo_list)
        
        for name in repo_manager.REPOS.keys():
            row = Gtk.ListBoxRow()
            repo_label = Gtk.Label(label=name)
            repo_label.set_hexpand(True)
            repo_label.set_ellipsize(Pango.EllipsizeMode.END)
            row.add(repo_label)
            repo_list.add(row)

    def create_status_tab(self, vbox):
        status_label = Gtk.Label("Status messages will appear here.")
        status_label.set_line_wrap(True)
        status_label.set_hexpand(True)
        vbox.pack_start(status_label, True, True, 0)
        self.status_label = status_label

    def on_repo_selected(self, listbox, row):
        repo_name = row.get_child().get_text()
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
            success, message = repo_manager.select_repo(repo_name)
            if success:
                self.show_message(message, Gtk.MessageType.INFO)
            else:
                self.show_message(message, Gtk.MessageType.ERROR)

    def show_progress(self, message):
        self.status_label.set_text(message)
        GLib.idle_add(self.update_status)

    def show_message(self, message, message_type):
        self.status_label.set_text(message)
        if message_type == Gtk.MessageType.ERROR:
            self.status_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 0, 0, 1))  # Red color
        else:
            self.status_label.override_color(Gtk.StateFlags.NORMAL, None)  # Reset color

    def refresh_repos(self, widget):
        # Placeholder for refreshing repository list
        self.show_message("Repository list refreshed.", Gtk.MessageType.INFO)

    def update_status(self):
        # Placeholder for updating status
        return False  # Stop the idle function

    def on_quit(self, widget):
        Gtk.main_quit()

def start_gui():
    win = RepoSelector()
    win.show_all()
    Gtk.main()
