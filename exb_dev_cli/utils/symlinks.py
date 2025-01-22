import subprocess
import sys
from pathlib import Path
import platform


def create_symlink(target: Path, link: Path):
    """
    Create a symbolic link with elevated privileges if necessary.
    """
    try:
        link.symlink_to(target)
        print(f"Symlink created: {link} -> {target}")
    except PermissionError:
        # If permission error, attempt elevation
        print("Admin privileges required to create the symlink.")
        _create_symlink_with_elevation(target, link)


def _create_symlink_with_elevation(target: Path, link: Path):
    """
    Attempt to create a symlink with elevated privileges, platform-specific.
    """
    system = platform.system()

    if system == "Windows":
        print("Asking For Admin Powershell")
        # Use PowerShell to create the symlink with elevation
        command = (
            f'powershell -Command "Start-Process powershell '
            f'-ArgumentList \'-Command New-Item -ItemType SymbolicLink -Path \'{link}\' -Target \'{target}\'\' -Verb RunAs"'
        )
    elif system in ["Linux", "Darwin"]:
        print("Run as sudo")
        # Use sudo for Unix-based systems
        command = f'sudo ln -s "{target}" "{link}"'

    else:
        raise NotImplementedError(f"Unsupported OS: {system}")

    # Run the command and check if it was successful
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Symlink created with elevated privileges: {link} -> {target}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create symlink with elevated privileges. Error: {e}")
