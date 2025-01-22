from pathlib import Path
import subprocess

from utils.symlinks import create_symlink


class ApplicationRepo:
    """
    Class to represent a cloned application repository that manages both widgets and application config symlinks.

    Attributes:
        app_name (str): The name of the application.
        app_repo_url (str): The URL of the application's Git repository.
        app_path (Path): The path where the application is cloned.
    """

    def __init__(self, app_name: str, app_repo_url: str, app_path: Path, exb_installation: Path = None):
        """
        Initializes the ApplicationRepo instance.

        Args:
            app_name (str): The name of the application.
            app_repo_url (str): The URL of the application's Git repository.
            app_path (Path): The path where the application is cloned.
        """
        self.app_name = app_name
        self.app_repo_url = app_repo_url
        self.app_path = app_path
        self.exb_installation = exb_installation


    @classmethod
    def clone(cls, app_name: str, app_repo_url: str, destination_path: Path, exb_installation: Path = None):
        """
        Clone the application repo from the given URL to the specified path.

        Args:
            app_name (str): The name of the application.
            app_repo_url (str): The URL of the application's Git repository.
            destination_path (Path): The destination path where the repo should be cloned.

        Returns:
            ApplicationRepo: The initialized ApplicationRepo object.
        """
        
        if Path(destination_path).exists():
            raise ValueError(f"Repository for {app_name} already exists.")
        else: 
            destination_path.mkdir(parents=True, exist_ok=True)
            # Clone the repository using subprocess to run a git command
            subprocess.run(["git", "clone", app_repo_url, str(destination_path)], check=True) 
        
        return cls(app_name, app_repo_url, destination_path, exb_installation)

    def create_widgets_symlink(self):
        """
        Create symlink for the app widgets folder in the Experience Builder client directory.

        Args:
        """

        widgets_symlink = self.exb_installation / 'client' / F"{self.app_name}_widgets"
        target_path = self.app_path / "Widgets"

        create_symlink(target_path, widgets_symlink)


    def create_app_config_symlink(self):
        """
        Create symlink for the app config folder in the Experience Builder server directory.

        Args:
        """
        config_symlink = self.exb_installation / 'server' / 'public' / '0'
        target_path = self.app_path / "AppConfig"

        create_symlink(target_path, config_symlink)


    def create_symlinks(self, exb_installation: str):
        """
        Create symlinks for the application repo, widgets, and app config in the Experience Builder installation.

        Args:
            exb_installation (ExperienceBuilderInstallation): The Experience Builder installation object.
        """
        if not self.app_path.exists():
            raise FileNotFoundError(f"Application repo {self.app_name} not found at {self.app_path}")

        self.exb_installation = exb_installation

        # Create the symlinks for widgets (both app and common, if available)
        self.create_widgets_symlink()

        # Create the symlink for the app config
        self.create_app_config_symlink()
