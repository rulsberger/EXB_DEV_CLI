import os
import pytest
import json
from pathlib import Path
from unittest.mock import patch
import click.testing
from exb_dev_cli.utils.app_manager import load_config, clone_repo
from exb_dev_cli.cli import cli
import shutil


def remove_readonly(func, path, excinfo):
    # Change the file permission to allow deletion
    os.chmod(path, 0o777)
    func(path)

@pytest.fixture
def sample_config(tmp_path):
    """Fixture to create a temporary config file."""
    config_data = {
        "Applications": {
            "testapp1": "https://ryanulsberger@bitbucket.org/piercecountywa-ss/testapp1.git",
        },
        "Core_Widgets": "https://ryanulsberger@bitbucket.org/piercecountywa-ss/exb-widgets.git"
    }
    config_file = tmp_path / "applications.json"
    config_file.write_text(json.dumps(config_data))
    return config_file


@pytest.fixture
def runner():
    """Fixture to create a Click CLI test runner."""
    return click.testing.CliRunner()


def test_load_config(sample_config):
    """Test that the config file is loaded correctly."""
    config = load_config(sample_config)
    assert "Applications" in config
    assert config["Applications"]["testapp1"] == "https://ryanulsberger@bitbucket.org/piercecountywa-ss/testapp1.git"


@patch("exb_dev_cli.cli.clone_single_repo")
def test_clone_single_repo_app(mock_clone_single_repo, sample_config, runner):
    print(f"Mock is: {mock_clone_single_repo}")
    dest_path = Path("./testapp1")

    """Test cloning an application repo."""
    result = runner.invoke(
        cli, ["clone_single_repo", "--app-name", "testapp1", "--config-file", str(sample_config)]
    )
        # Print call args to debug
    print(f"Mock was called with: {mock_clone_single_repo.call_args}")
    print(result)
    try:
        assert True == True
        # Assert that clone_single_repo was called with the expected arguments
        mock_clone_single_repo.assert_called_once_with(
            "testapp1", str(sample_config)
        )
        # assert result.exit_code == 0
        # assert "Successfully cloned app1" in result.output

    finally:
        # Cleanup: Ensure the directory is removed if it exists, even if the test fails
        if dest_path.exists():
            shutil.rmtree(dest_path, onerror=remove_readonly)



# @patch("exb_dev_cli.utils.app_manager.clone_repo")
# def test_clone_single_repo_core_widgets(mock_clone_repo, sample_config, runner):
#     dest_path = Path("./exb-widgets")

#     """Test cloning the Core_Widgets repo."""
#     result = runner.invoke(
#         cli, ["clone-single-repo", "--app-name", "Core_Widgets", "--config-file", str(sample_config)]
#     )
#     assert result.exit_code == 0
#     mock_clone_repo.assert_called_once_with(
#         "https://ryanulsberger@bitbucket.org/piercecountywa-ss/exb-widgets.git", dest_path, None
#     )
#     assert "Successfully cloned Core_Widgets" in result.output

#     # CleanUp 
#     if dest_path.exists:
#         dest_path.rmdir()

# def test_clone_single_repo_invalid_app(sample_config, runner):
#     """Test error handling for a non-existent application."""
#     result = runner.invoke(
#         cli, ["clone-single-repo", "--app-name", "invalid_app", "--config-file", str(sample_config)]
#     )
#     assert result.exit_code != 0
#     assert "Repository for invalid_app not found" in result.output

# @patch("exb_dev_cli.utils.app_manager.clone_repo", side_effect=Exception("Clone error"))
# def test_clone_repo_error(mock_clone_repo, sample_config, runner):
#     """Test handling of cloning errors."""
#     result = runner.invoke(
#         cli, ["clone-single-repo", "--app-name", "app1", "--config-file", str(sample_config)]
#     )
#     assert result.exit_code != 0
#     assert "Error: Clone error" in result.output
