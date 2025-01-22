import os
import subprocess
import pytest
import json
from pathlib import Path
import requests
import zipfile

def load_config(file_path):
    """
    Loads a JSON configuration file.

    Args:
        file_path (str): Path to the JSON configuration file.

    Returns:
        dict: The loaded JSON data.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        return json.load(f)

def get_repo_details(app_name, config_file_path):
    """
    Validate the app_name and return the repository URL and type.

    Args:
        app_name (str): The name of the app to retrieve from the config.
        config_file_path (str or Path): Path to the config file.

    Returns:
        (str, str): Repository URL and type ("core-widgets" or "application").
    """
    config = load_config(config_file_path)

    if app_name == "core-widgets":
        repo_url = config.get("Core_Widgets")
        repo_type = "core-widgets"
    elif app_name in config.get("Applications", {}):
        repo_url = config["Applications"][app_name]
        repo_type = "application"
    else:
        raise ValueError(f"'{app_name}' not found in the configuration file.")

    return repo_url, repo_type