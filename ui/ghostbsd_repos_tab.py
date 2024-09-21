from gi.repository import Gtk
import repo.ghostbsd_repo_manager as ghostbsd_repo_manager

class GhostBSDReposTab(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.create_repo_ui()

    def create_repo_ui(self):
        label = Gtk.Label(label="Select a GhostBSD Repository")
        self.append(label)

        # Create a ComboBox to list GhostBSD repositories
        self.repo_combo = Gtk.ComboBoxText()
        repos = ghostbsd_repo_manager.list_repos()

        for repo in repos:
            self.repo_combo.append_text(repo)

        self.repo_combo.connect("changed", self.on_repo_selected)
        self.append(self.repo_combo)

    def on_repo_selected(self, combo):
        repo_name = combo.get_active_text()
        if repo_name:
            success, message = ghostbsd_repo_manager.update_config(repo_name)
            print(message)  # Display message in the console for now

