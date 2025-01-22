from pathlib import Path

from ApplicationRepo import ApplicationRepo

class ExperienceBuilderInstallation:
    """
    Class to manage the installed Experience Builder and the associated app repositories.

    Attributes:
        exb_path (Path): The path to the Experience Builder installation.
        exb_version (str): The version of the Experience Builder installation.
        apps (dict): A dictionary of ApplicationRepo instances, mapping app names to repo instances.
    """

    def __init__(self, exb_path: Path, exb_version: str):
        """
        Initializes the ExperienceBuilderInstallation instance and loads installed apps.

        Args:
            exb_path (Path): The path to the Experience Builder installation.
            exb_version (str): The version of the Experience Builder installation.
        """
        self.exb_path = exb_path
        self.exb_version = exb_version
        self.apps = {}  # A dictionary to hold ApplicationRepo instances for each app

        # Load installed apps
        self._load_installed_apps()

    @property
    def client_directory(self):
        """Returns the client directory inside the Experience Builder installation.

        Returns:
            Path: The path to the client directory.

        Raises:
            FileNotFoundError: If the client directory is not found.
        """
        client_dir = self.exb_path / "client"
        if client_dir.exists():
            return client_dir
        raise FileNotFoundError(f"Client directory not found at {client_dir}")

    @property
    def server_directory(self):
        """Returns the server directory inside the Experience Builder installation.

        Returns:
            Path: The path to the server directory.

        Raises:
            FileNotFoundError: If the server directory is not found.
        """
        server_dir = self.exb_path / "server"/ "public" / "apps"
        if server_dir.exists():
            return server_dir
        raise FileNotFoundError(f"Server directory not found at {server_dir}")

    def _load_installed_apps(self):
        """
        Loads the installed applications from the `server/public/apps` directory and associates them with their repos.
        """
        apps_path = self.server_directory / "public" / "apps"
        if apps_path.exists():
            for app_folder in apps_path.iterdir():
                if app_folder.is_dir():
                    app_name = app_folder.name
                    app_repo_path = Path(f"repos/{app_name}")  # Assuming repo is in a "repos" directory
                    if app_repo_path.exists():
                        app_repo = ApplicationRepo(app_repo_path, app_name)
                        self.apps[app_name] = app_repo

    def install_app(self, app_name: str, app_repo_url: str, branch: str = "main"):
        """
        Installs a new app by cloning the repo and creating symlinks for widgets and app config.

        Args:
            app_name (str): The name of the app.
            app_repo_url (str): The URL of the app's repository.
            branch (str): The branch to clone. Defaults to 'main'.
        """
        if app_name in self.apps:
            raise ValueError(f"App {app_name} is already installed.")

        app_repo_path = Path(f"./{app_name}")
        # app_repo = ApplicationRepo(app_name, app_repo_url, app_repo_path)
        # ApplicationRepo().clone
        # Clone the repo
        app_repo = ApplicationRepo.clone(app_name, app_repo_url, app_repo_path, self.exb_path)

    def config_app(self, app_name: str, app_repo_url: str):
        """
        Installs a new app by cloning the repo and creating symlinks for widgets and app config.

        Args:
            app_name (str): The name of the app.
        """
        # Add the app repo to the installed apps
        app_repo_path = Path(f"./{app_name}")
        self.apps[app_name] = app_repo_path
        
        app_repo = ApplicationRepo(app_name, app_repo_url, app_repo_path, self.exb_path)

        # # Create the symlinks for the app
        app_repo.create_symlinks(self.exb_path)

    def remove_app(self, app_name: str):
        """
        Removes an app and its associated symlinks.

        Args:
            app_name (str): The name of the app to remove.
        """
        if app_name in self.apps:
            app_repo = self.apps[app_name]
            app_repo.remove_symlinks()  # Method to remove the symlinks (to be implemented)
            del self.apps[app_name]
        else:
            raise ValueError(f"App {app_name} not found.")

if __name__ == "__main__":
    exb_install_path = Path("ArcGISExperienceBuilder")

    exb_install = ExperienceBuilderInstallation(exb_install_path, "v1.16")
    # exb_install.install_app("apptemplate", "https://ryanulsberger@bitbucket.org/piercecountywa-ss/apptemplate.git")
    exb_install.config_app("apptemplate", "https://ryanulsberger@bitbucket.org/piercecountywa-ss/apptemplate.git")
    print(exb_install.apps)