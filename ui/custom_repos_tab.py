from gi.repository import Gtk
import repo.custom_repo_manager as custom_repo_manager

class CustomReposTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Load custom repositories from file
        custom_repo_manager.load_repos_from_file()

        self.create_custom_repo_ui()

    def create_custom_repo_ui(self):
        label = Gtk.Label(label="Manage Custom Repositories")
        self.append(label)

        # Create a listbox to display custom repositories
        self.repo_listbox = Gtk.ListBox()
        self.update_repo_list()
        self.append(self.repo_listbox)

        # Create a horizontal box for Add/Remove buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        # Add button
        add_button = Gtk.Button(label="Add Repository")
        add_button.connect("clicked", self.on_add_repo_clicked)
        button_box.append(add_button)

        # Remove button
        remove_button = Gtk.Button(label="Remove Repository")
        remove_button.connect("clicked", self.on_remove_repo_clicked)
        button_box.append(remove_button)

        self.append(button_box)

    def update_repo_list(self):
        # Remove all children from the listbox
        row = self.repo_listbox.get_first_child()
        while row is not None:
            next_row = row.get_next_sibling()
            self.repo_listbox.remove(row)
            row = next_row

        # Get the list of custom repositories from the manager
        repos = custom_repo_manager.list_custom_repos()

        # Add each repository to the listbox
        for repo in repos:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=repo)
            row.set_child(label)
            self.repo_listbox.append(row)

    def on_add_repo_clicked(self, widget):
        # Get the parent window (main application window) to set as transient_for
        parent_window = self.get_native()

        # Create a dialog to get repository details
        dialog = Gtk.Dialog(transient_for=parent_window, title="Add a Custom Repository (as superuser)", modal=True)

        # Create a grid for the form layout
        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        
        # Repository Name
        repo_name_label = Gtk.Label(label="Repository Name:")
        repo_name_entry = Gtk.Entry()

        # Latest URL
        latest_url_label = Gtk.Label(label="Latest URL:")
        latest_url_entry = Gtk.Entry()

        # Base URL
        base_url_label = Gtk.Label(label="Base URL:")
        base_url_entry = Gtk.Entry()

        # Public Key (Optional)
        public_key_label = Gtk.Label(label="Public Key (Optional):")
        public_key_entry = Gtk.Entry()

        # Add the widgets to the grid
        grid.attach(repo_name_label, 0, 0, 1, 1)
        grid.attach(repo_name_entry, 1, 0, 1, 1)

        grid.attach(latest_url_label, 0, 1, 1, 1)
        grid.attach(latest_url_entry, 1, 1, 1, 1)

        grid.attach(base_url_label, 0, 2, 1, 1)
        grid.attach(base_url_entry, 1, 2, 1, 1)

        grid.attach(public_key_label, 0, 3, 1, 1)
        grid.attach(public_key_entry, 1, 3, 1, 1)

        dialog.get_content_area().append(grid)

        # Add OK and Cancel buttons to the dialog
        dialog.add_button("OK", Gtk.ResponseType.OK)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)

        # Connect the response signal
        dialog.connect("response", self.on_add_repo_response, repo_name_entry, latest_url_entry, base_url_entry, public_key_entry)

        # Present the dialog to the user
        dialog.present()

    def on_add_repo_response(self, dialog, response_id, repo_name_entry, latest_url_entry, base_url_entry, public_key_entry):
        if response_id == Gtk.ResponseType.OK:
            repo_name = repo_name_entry.get_text()
            latest_url = latest_url_entry.get_text()
            base_url = base_url_entry.get_text()
            public_key = public_key_entry.get_text() if public_key_entry.get_text() else None

            # Ensure repository name and URLs are not empty
            if repo_name and latest_url and base_url:
                success, message = custom_repo_manager.add_custom_repo(repo_name, latest_url, base_url, public_key)
                self.update_repo_list()
                print(message)  # Print success or error message for now

        dialog.destroy()

    def on_remove_repo_clicked(self, widget):
        selected_row = self.repo_listbox.get_selected_row()

        if selected_row:
            repo_name = selected_row.get_child().get_label()
            success, message = custom_repo_manager.remove_custom_repo(repo_name)
            self.update_repo_list()
            print(message)  # Print success or error message for now

