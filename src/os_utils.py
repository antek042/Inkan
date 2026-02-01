import subprocess

def create_flatpaks_copy(dest):
        result = subprocess.run(
                ["flatpak", "list", "--user", "--columns=application"],
                capture_output=True,
                text=True,
        )
        flatpaks = result.stdout.strip().split("\n")
        with open(f"{dest}/flatpks_copy.txt", "w") as f:
                for flatpak in flatpaks:
                        f.write(flatpak + "\n")