from unittest import mock
import pytest
from src.applications.settings.container import get_deps_container


@pytest.fixture
def mock_config_paths(config_folder):
    """Mock the settings paths for testing dependency container.

    Args:
        config_folder: Path to the test configuration folder.

    Yields:
        mock.MagicMock: The mocked settings paths.
    """
    with mock.patch(
        "src.applications.settings.container.SettingsPaths"
    ) as mock_settings_paths:
        settings_path_mock = mock.Mock()
        settings_path_mock().CONFIG_PATH = config_folder + "/config.json"
        mock_settings_paths.side_effect = settings_path_mock
        yield mock_settings_paths


def test_get_container(mock_config_paths):
    """Test that the dependency container is properly initialized."""
    container = get_deps_container()
    assert container is not None
