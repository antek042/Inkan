import os
import tarfile
import zstandard as zstd
import subprocess

def compress_folder(folder_path, output_path, level=10):
    """
    Compresses a folder into a .tar.zst archive.

    Args:
        folder_path (str): Path to the folder to compress.
        output_path (str): Path where the compressed archive will be saved.
        level (int, optional): Compression level (default is 10).

    Notes:
        Uses Zstandard compression inside a TAR container.
    """
    tar_path = f"{output_path}.tar"
    zst_path = f"{output_path}.tar.zst"

    with tarfile.open(tar_path, "w:tar") as tf:
        tf.add(folder_path, arcname=".")

    compressor = zstd.ZstdCompressor(level)

    with open(tar_path, "rb") as f_in, open(zst_path, "wb") as f_out:
        compressor.copy_stream(f_in, f_out)

    os.remove(tar_path)


def decompress_folder(file_path, output_path):
    """
    Decompresses a .tar.zst archive into a specified folder.

    Args:
        file_path (str): Path to the .tar.zst archive to decompress.
        output_path (str): Path where the decompressed folder will be created.

    Notes:
        Extracts all files from the Zstandard-compressed TAR archive into
        the specified output directory, preserving the folder structure.
    """
    if not os.path.isdir(output_path):
        os.makedirs(output_path, exist_ok=True)

    tar_path = os.path.join(output_path, "tmp_extract.tar")

    dctx = zstd.ZstdDecompressor()

    with open(file_path, "rb") as input_f, open(tar_path, "wb") as output_f:
        dctx.copy_stream(input_f, output_f)

    with tarfile.open(tar_path, "r") as tf:
        tf.extractall(path=output_path, filter="data")

    os.remove(tar_path)


def get_devices_dict(platform):
    """
    Returns a list of available external drives.

    Args:
        platform (str): OS name.

    Returns:
        dict: A dictionary of available external drives.
    """
    devices = {}
    if platform == "Linux":
        import pyudev

        context = pyudev.Context()
        for device in context.list_devices(subsystem="block", DEVTYPE="disk"):
            if device.get("ID_BUS") == "usb":
                with open("/proc/mounts") as f:
                    for line in f:
                        if device.device_node in line:
                            devices[device.get("ID_MODEL")] = line.split()[1]
    elif platform == "Windows":
        import wmi

        context = wmi.WMI()
        for disk in context.Win32_DiskDrive():
            if "USB" in disk.InterfaceType:
                for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                    for logical_disk in partition.associators(
                        "Win32_LogicalDiskToPartition"
                    ):
                        devices[disk.Model] = logical_disk.DeviceID

    return devices


def detect_desktop_environment():
    """
    Detects the current desktop environment from environment variables.

    Returns:
        str: Name of the desktop environment (e.g., 'GNOME', 'KDE Plasma', 'Cinnamon').
    """
    xdg = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    session = os.environ.get("DESKTOP_SESSION", "").lower()

    if "gnome" in xdg or "gnome" in session:
        return "gnome"
    elif "kde" in xdg or "kde" in session:
        return "kde"
    elif "cinnamon" in xdg or "cinnamon" in session:
        return "cinnamon"

    return "unknown"

def set_wallpaper(file_path):
    """
    Sets the desktop wallpaper to the specified image file.

    Args:
        file_path (str): Path to the image file to set as wallpaper.
    """
    env = detect_desktop_environment()
    if env is "gnome":
        subprocess.run([
            "gsettings", "set",
            "org.gnome.desktop.background",
            "picture-uri-dark", f"file://{file_path}",
        ])
    elif env is "kde":
        subprocess.run([
            "plasma-apply-wallpaperimage",
            file_path
        ])
    elif env is "cinnamon":
        subprocess.run([
            "gsettings", "set",
            "org.cinnamon.desktop.background",
            "picture-uri", f"file://{file_path}",
        ])


def get_installed_windows_programs():
    """
    Returns the set of installed programs on a Windows system.

    Returns:
        programs (set): Set of installed programs
    """
    import winreg

    uninstall_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ]

    programs = set()
    for key_path in uninstall_keys:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)
                try:
                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    programs.add(name)
                except FileNotFoundError:
                    continue
        except FileNotFoundError:
            continue

    return programs
