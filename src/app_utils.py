import subprocess
import requests
import gazpacho

def download_from_flathub(app_id):
    """
    Downloads an application from Flathub using Flatpak.

    Args:
        app_id (str): The Flatpak application ID.

    Returns:
        bool: True if installation succeeded, False otherwise.
    """
    
    try:
        subprocess.run(["flatpak", "install", "-y", "flathub", app_id], check=True)
        return True
    except:
        return False

def search_in_flathub(app):
    """
    Searches for applications in Flathub.

    Args:
        app (str): Search term for the application.

    Returns:
        list[dict]: List of application results from Flathub API.
    """

    flathub_url = f"https://flathub.org/api/v2/compat/apps/search/{app}"
    responses = requests.get(flathub_url, timeout=10)
    responses.raise_for_status()
    return responses.json()

def search_for_app(name):
    """
    Finds the Flatpak application ID for a given search term.

    Args:
        name (str): The name or part of the name of the application.

    Returns:
        str or None: The Flatpak application ID if found, otherwise None.
    """

    results = search_in_flathub(name)
    for result in results:
        app_id = result["flatpakAppId"]
        if name.lower() in app_id.lower():
            return app_id
    return None

def search_for_alternatives(app):
    """
    Searches for alternative applications using openalternative.co and checks if they are available on Flathub.

    Args:
        app (str): The name or ID of the application to find alternatives for.

    Returns:
        str or None: The Flatpak application ID of the first alternative found on Flathub, or None if none found.
    """
    URL = f"https://openalternative.co/alternatives/{app.replace(' ', '-').lower()}"
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
        app_id = search_for_app(name)
        if app_id is not None:
            return app_id

    return None