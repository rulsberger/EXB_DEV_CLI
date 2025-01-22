from pathlib import Path

class ApplicationConfig:
    """
    Class to manage the symlinks for the application config files in the Experience Builder installation.

    Attributes:
        app_name (str): The name of the application.
        app_path (Path): The path to the application's repo.
    """

    def __init__(self, app_name: str, app_path: Path):
        """
        Initializes the ApplicationConfig instance.

        Args:
            app_name (str): The name of the application.
            app_path (Path): The path to the application's repo.
        """
        self.app_name = app_name
        self.app_path = app_path

    def create_app_config_symlink(self, exb_server_path: Path):
        """
        Create the symlink for the application config folder.

        Args:
            exb_server_path (Path): The path to the Experience Builder server directory.
        """
        config_symlink = exb_server_path / self.app_name / "config"
        if config_symlink.exists():
            config_symlink.unlink()
        config_symlink.symlink_to(self.app_path / "config")
