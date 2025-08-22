import pytest
from unittest.mock import patch, MagicMock
from app_utils import download_from_flathub, search_for_alternatives, search_in_flathub, search_for_app

def test_download_from_flathub_runs_flatpak_install_successfully():
    """Tests if download_from_flathub calls flatpak install with correct parameters."""
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = None
        download_from_flathub("org.mozilla.firefox")
        mock_run.assert_called_once_with(
            ["flatpak", "install", "-y", "flathub", "org.mozilla.firefox"],
            check=True,
        )


def test_download_from_flathub_returns_false_on_exception():
    """Tests if download_from_flathub returns False when an exception occurs."""

    with patch("subprocess.run", side_effect=Exception("fail")) as mock_run:
        result = download_from_flathub("org.mozilla.firefox")
        assert result is False

@patch("requests.get")
def test_search_in_flathub_returns_app_list(mock_requests_get):
    """Tests if search_in_flathub returns a list of apps retrieved from the Flathub API."""

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [{"flatpakAppId": "org.gimp.GIMP"}]
    mock_requests_get.return_value = mock_response

    result = search_in_flathub("gimp")
    assert result == [{"flatpakAppId": "org.gimp.GIMP"}]

@patch("app_utils.search_in_flathub")
def test_search_for_app_returns_app_id_on_success(mock_search):
    """Tests if search_for_app returns the app ID when an app is found."""

    mock_search.return_value = [{"flatpakAppId": "org.gimp.GIMP"}]
    result = search_for_app("gimp")
    assert result == "org.gimp.GIMP"

@patch("app_utils.search_in_flathub")
def test_search_for_app_returns_none_when_no_app_found(mock_search):
    """Tests if search_for_app returns None when no app is found."""

    mock_search.return_value = []
    result = search_for_app("gimp")
    assert result is None

@patch("gazpacho.get")
@patch("gazpacho.Soup")
@patch("app_utils.search_for_app")
def test_search_for_alternatives_returns_app_id_when_found(mock_search_for_app, mock_soup_class, mock_get):
    """Tests if search_for_alternatives returns the correct app ID when an alternative is found."""

    mock_get.return_value =  "<html></html>"
    
    fake_headers = [MagicMock(attrs={"id": "alt-app-1"}), MagicMock(attrs={"id": "alt-app-2"})]

    mock_soup_instance = MagicMock()
    mock_soup_instance.find.return_value = fake_headers
    mock_soup_class.return_value = mock_soup_instance

    mock_search_for_app.side_effect = [None, "org.flathub.alt-app-2"]

    result = search_for_alternatives("Firefox")
    assert result == "org.flathub.alt-app-2"


@patch("gazpacho.get")
@patch("gazpacho.Soup")
@patch("app_utils.search_for_app")
def test_search_for_alternatives_returns_none_when_not_found(mock_search_for_app, mock_soup_class, mock_get):
    """Tests if search_for_alternatives returns None when no alternatives are found."""

    mock_get.return_value =  "<html></html>"
    
    fake_headers = [MagicMock(attrs={"id": "alt-app-1"}), MagicMock(attrs={"id": "alt-app-2"})]

    mock_soup_instance = MagicMock()
    mock_soup_instance.find.return_value = fake_headers
    mock_soup_class.return_value = mock_soup_instance

    mock_search_for_app.side_effect = [None, None]

    result = search_for_alternatives("Firefox")
    assert result is None