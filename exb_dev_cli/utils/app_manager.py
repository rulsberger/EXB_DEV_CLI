import os
import subprocess
import pytest
import json
from pathlib import Path
import requests
import zipfile

from symlinks import create_symlinks_to_experience_builder
from config import load_config, get_repo_details


VERSIONS_JSON = Path("./exb_dev_cli/versions.json")


def clone_repo(repo_url, destination_dir, branch=None):
    """
    Clones a Git repository to the specified directory.

    Args:
        repo_url (str): The URL of the Git repository to clone.
        destination_dir (str): The directory to clone the repository into.
        branch (str, optional): The branch to check out after cloning. Defaults to None.

    Returns: 
        destination_dir (str): The directory where Experience Builder will be installed.

    Raises:
        subprocess.CalledProcessError: If the `git clone` or `git checkout` command fails.
    """
    subprocess.run(['git', 'clone', repo_url, destination_dir], check=True)
    if branch:
        subprocess.run(['git', 'checkout', branch], cwd=destination_dir, check=True)
    
    return destination_dir

def clone_repos_from_config(config_file, destination, branch=None):
    """
    Clones repositories specified in the configuration JSON file.

    Args:
        config_file (str): Path to the JSON configuration file containing the repository URLs.
        destination (str): The directory where the repositories will be cloned.
        branch (str, optional): The branch to check out for each repository. Defaults to None.

    Returns: 
        destination_dir (str): The directory where Experience Builder will be installed.

    Raises:
        Exception: If there is an error loading or cloning the repositories.
    """
    config = load_config(config_file)
    
    # Clone Applications
    apps = config.get('Applications', {})
    for app, repo_url in apps.items():
        app_dest_dir = Path(destination) / app
        print(f"Cloning {app} from {repo_url} into {app_dest_dir}")
        clone_repo(repo_url, app_dest_dir, branch)
    
    # Clone Core Widgets
    core_widgets_url = config.get('Core_Widgets')
    if core_widgets_url:
        core_widgets_dest_dir = Path(destination) / "core_widgets"
        print(f"Cloning Core Widgets from {core_widgets_url} into {core_widgets_dest_dir}")
        clone_repo(core_widgets_url, core_widgets_dest_dir, branch)

    return 

def install_experience_builder(version, destination_dir):
    """
    Downloads and installs the specified version of Experience Builder.

    Args:
        version (str): The version of Experience Builder to install.
        destination_dir (str): The directory where Experience Builder will be installed.

    Returns: 
        destination_dir (str): The directory where Experience Builder will be installed.

    Raises:
        ValueError: If the version is not found in the versions.json.
        requests.exceptions.RequestException: If there is an error downloading the file.
        zipfile.BadZipFile: If the downloaded file is not a valid zip file.
    """
    with open(VERSIONS_JSON, 'r') as f:
        versions = json.load(f).get('Experience_Builder', {})
    
    if version not in versions:
        raise ValueError(f"Version {version} not found in versions.json.")
    
    url = versions[version]
    print(f"Downloading Experience Builder version {version} from {url}...")
    
    # Download the ZIP file
    response = requests.get(url)
    response.raise_for_status()
    
    # Save the ZIP file
    zip_file_path = Path(destination_dir) / f"experience_builder_{version}.zip"
    with open(zip_file_path, 'wb') as f:
        f.write(response.content)
    
    # Unzip the file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_dir)
    
    print(f"Experience Builder version {version} installed in {destination_dir}.")

    return destination_dir

def clone_and_symlink(app_name, config_file_path, exb_install_path):
    """
    Clones a specified application repository and creates symlinks to the Experience Builder installation.

    Args:
        app_name (str): Name of the application to clone.
        config_file_path (str): Path to the config file containing repository URLs.
        exb_install_path (str): Path to the Experience Builder installation.
    """
    app_repo_url, repo_type = get_repo_details(app_name, config_file_path)      

    # Clone the repo
    app_repo_path = Path(f"./{app_name}")
    app_repo_path = clone_repo(app_repo_url, app_repo_path)

    # Create symlinks
    if Path(exb_install_path).exists():
        create_symlinks_to_experience_builder(app_repo_path, exb_install_path)
        print(f"{app_name} setup complete with symlinks.")
    else: 
        print('An valid installation path to experience builder is needed.')