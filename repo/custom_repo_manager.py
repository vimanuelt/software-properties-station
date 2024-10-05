import os

# Define the directory where configuration files will be stored
config_dir = '/etc/pkg'

# Initialize an empty list of custom repositories
custom_repos = []

def load_repos_from_file():
    """
    Load custom repositories from the configuration directory.
    """
    global custom_repos
    custom_repos = []
    for filename in os.listdir(config_dir):
        if filename.endswith('.conf') and filename != 'GhostBSD.conf':
            custom_repos.append(filename.replace('.conf', ''))

def save_repo_to_file(repo_name, latest_url, base_url, public_key=None):
    """
    Save a custom repository configuration to a file.
    If no public key is provided, the signature_type and pubkey lines are excluded.
    """
    config_file_path = os.path.join(config_dir, f"{repo_name}.conf")
    
    # Construct the configuration
    config_content = f"{repo_name}: {{\n  url: \"{latest_url}\",\n"
    
    # If a public key is provided, include the signature_type and pubkey lines
    if public_key:
        config_content += f"  signature_type: \"pubkey\",\n  pubkey: \"{public_key}\",\n"
    
    config_content += "  enabled: yes\n}}\n"
    
    # Add the base URL configuration
    config_content += f"{repo_name}-base: {{\n  url: \"{base_url}\",\n"
    
    # If a public key is provided, include the signature_type and pubkey lines for base URL as well
    if public_key:
        config_content += f"  signature_type: \"pubkey\",\n  pubkey: \"{public_key}\",\n"
    
    config_content += "  enabled: yes\n}}\n"

    # Write the configuration to the file
    with open(config_file_path, 'w') as config_file:
        config_file.write(config_content)

def list_custom_repos():
    """
    Returns a list of custom repositories.
    """
    return custom_repos

def add_custom_repo(repo_name, latest_url, base_url, public_key=None):
    """
    Adds a custom repository and creates a config file for it.
    """
    if repo_name not in custom_repos:
        custom_repos.append(repo_name)
        save_repo_to_file(repo_name, latest_url, base_url, public_key)
        return True, f"Custom repository '{repo_name}' added successfully."
    else:
        return False, f"Repository '{repo_name}' already exists."

def remove_custom_repo(repo_name):
    """
    Removes a custom repository and deletes the corresponding config file.
    """
    if repo_name in custom_repos:
        custom_repos.remove(repo_name)
        config_file_path = os.path.join(config_dir, f"{repo_name}.conf")
        if os.path.exists(config_file_path):
            os.remove(config_file_path)
        return True, f"Custom repository '{repo_name}' removed successfully."
    return False, f"Repository '{repo_name}' not found."

