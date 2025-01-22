import click
from pathlib import Path

from exb_dev_cli.utils.app_manager import load_config, get_repo_details, install_experience_builder, clone_repos_from_config, clone_repo, clone_and_symlink


@click.group()
def cli():
    """
    Experience Builder CLI for managing installations and repositories.
    
    This command-line tool allows users to install specific versions of Experience Builder
    and clone repositories based on a configuration file.
    """
    pass

@click.command()
@click.option('--version', required=True, help="Experience Builder version to install.")
@click.option('--destination', default='./', help="Directory where to install Experience Builder.")
def install(version, destination):
    """
    Install a specific version of Experience Builder.

    Args:
        version (str): The version of Experience Builder to install.
        destination (str): The directory where to install Experience Builder.
    
    Raises:
        click.ClickException: If an error occurs during installation.
    """
    try:
        install_experience_builder(version, destination)
        click.echo(f"Successfully installed Experience Builder version {version}.")
    except Exception as e:
        click.echo(f"Error: {e}")

@click.command()
@click.option('--config-file', default='applications.json', help="Path to the applications config file.")
@click.option('--destination', default='./', help="Directory where to clone repositories.")
@click.option('--branch', default=None, help="Branch to check out for each repo.")
def clone(config_file, destination, branch):
    """
    Clone repositories from the config file.

    Args:
        config_file (str): Path to the JSON configuration file containing the repository URLs.
        destination (str): The directory where the repositories will be cloned.
        branch (str, optional): The branch to check out for each repository. Defaults to None.
    
    Raises:
        click.ClickException: If an error occurs while cloning repositories.
    """
    try:
        clone_repos_from_config(config_file, destination, branch)
        click.echo(f"Successfully cloned repositories from {config_file} into {destination}.")
    except Exception as e:
        click.echo(f"Error: {e}")

@click.command()
@click.option('--app-name', required=True, help="The name of the application or 'Core_Widgets' to clone.")
@click.option('--config-file', default='applications.json', help="Path to the applications config file.")
@click.option('--destination', default='./', help="Directory where to clone the repository.")
@click.option('--branch', default=None, help="Branch to check out for the repository.")
def clone_single_repo(app_name, config_file, destination, branch):
    """
    Clone a single repository from the config file, including Core_Widgets.

    Args:
        app_name (str): The name of the application or 'Core_Widgets' to clone.
        config_file (str): Path to the JSON configuration file containing the repository URLs.
        destination (str): The directory where the repository will be cloned.
        branch (str, optional): The branch to check out for the repository. Defaults to None.
    
    Raises:
        click.ClickException: If an error occurs while cloning the repository.
    """
    app_repo_url, repo_type = get_repo_details(app_name, config_file)
    try:
        if not app_repo_url:
            raise ValueError(f"Repository for {app_name} not found in the config file.")
        
        app_dest_dir = Path(destination) / app_name
        print(f"Cloning {app_name} from {app_repo_url} into {app_dest_dir}")
        clone_repo(app_repo_url, app_dest_dir, branch)
        click.echo(f"Successfully cloned {app_name} from {app_repo_url} into {app_dest_dir}.")
    
    except Exception as e:
        click.echo(f"Error: {e}")

@click.command()
@click.option("--app-name", required=True, help="Name of the application to clone.")
@click.option("--config-file", required=True, type=click.Path(exists=True), help="Path to the applications.json config file.")
@click.option("--exb-path", required=True, type=click.Path(exists=True), help="Path to the Experience Builder installation.")
def clone_app_and_symlink(app_name, config_file, exb_path):
    """
    CLI command to clone an app repo and create symlinks.

    Args:
        app_name (str): The name of the application or 'Core_Widgets' to clone.
        config_file (str): Path to the JSON configuration file containing the repository URLs.
        exb_path (str): The directory of an install of Experience Builder Developer Edition.
    
    Raises:
        click.ClickException: If an error occurs while cloning the repository.
    """
    clone_and_symlink(app_name, config_file, exb_path)

cli.add_command(install)
cli.add_command(clone)
cli.add_command(clone_single_repo)
cli.add_command(clone_app_and_symlink)

if __name__ == '__main__':
    cli()
