import pytest
from unittest.mock import patch, MagicMock
from app_utils import download_from_flathub, search_for_alternatives


def test_download_from_flathub_success():
    """Tests that download_from_flathub uses correct parameters."""

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = None
        download_from_flathub("org.mozilla.firefox")
        mock_run.assert_called_once_with(
            ["flatpak", "install", "-y", "flathub", "org.mozilla.firefox"],
            check=True,
        )


def test_download_from_flathub_failure():
    """Tests that download_from_flathub correctly deals with exceptions."""

    with patch("subprocess.run", side_effect=Exception("fail")) as mock_run:
        result = download_from_flathub("org.mozilla.firefox")
        assert result is None


@patch("gazpacho.get")
@patch("gazpacho.Soup")
@patch("requests.get")
def test_search_for_alternatives_found(mock_requests_get, mock_soup, mock_gazpacho_get):
    """Tests that search_for_alternatives returns correct app id."""

    mock_gazpacho_get.return_value = "<html></html>"

    mock_header = MagicMock()
    mock_header.text = "GIMP"
    mock_soup.return_value.find.return_value = [mock_header]

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [{"flatpakAppId": "org.gimp.GIMP"}]
    mock_requests_get.return_value = mock_response

    result = search_for_alternatives("photoshop")
    assert result == "org.gimp.GIMP"


@patch("gazpacho.get")
@patch("gazpacho.Soup")
@patch("requests.get")
def test_search_for_alternatives_not_found(
    mock_requests_get, mock_soup, mock_gazpacho_get
):
    """Tests that search_for_alternatives returns nothing when no alternatives are found."""

    mock_gazpacho_get.return_value = "<html></html>"

    mock_header = MagicMock()
    mock_header.text = "GIMP"
    mock_soup.return_value.find.return_value = [mock_header]

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [{"flatpakAppId": "org.inkan.INKAN"}]
    mock_requests_get.return_value = mock_response

    result = search_for_alternatives("photoshop")
    assert result == ""
