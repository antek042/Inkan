import subprocess
import requests

def download_from_flathub(app):
    """
    Downloads an application from Flathub using Flatpak.

    Args:
        app (str): The Flatpak application ID.
    """
    url = f"https://flathub.org/api/v2/compat/apps/search/{app}"
    response = requests.get(url=url)
    response.raise_for_status()
    data = response.json()
    try:
        subprocess.run(["flatpak", "install", "-y", "flathub", data[0]["flatpakAppId"]],
                check=True)
    except:
        return