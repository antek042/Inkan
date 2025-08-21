import subprocess
import requests
import gazpacho


def download_from_flathub(app):
    """
    Downloads an application from Flathub using Flatpak.

    Args:
        app (str): The Flatpak application ID.
    """

    try:
        subprocess.run(["flatpak", "install", "-y", "flathub", app], check=True)
    except:
        return


def search_for_alternatives(app):
    """
    Searches for alternative applications to the given app using openalternative.co
    and checks if they are available on Flathub.

    Args:
        app (str): The name or ID of the application to find alternatives for.

    Returns:
        str: The name of the first alternative found on Flathub, or an empty string if none found.
    """

    URL = f"https://openalternative.co/alternatives/{app}"
    html = gazpacho.get(URL)
    soup = gazpacho.Soup(html)
    data = soup.find(
        "h2",
        {
            "class": "font-display font-semibold text-2xl tracking-tight md:text-3xl leading-tight! truncate underline decoration-transparent group-hover:decoration-foreground/30"
        },
        mode="all",
    )

    for header in data:
        name = header.text
        flathub_url = f"https://flathub.org/api/v2/compat/apps/search/{name}"
        responses = requests.get(flathub_url)
        responses.raise_for_status()
        app_id = responses.json()[0]["flatpakAppId"]
        if name in app_id:
            return app_id

    return ""
