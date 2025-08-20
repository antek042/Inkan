import tarfile
import zstandard as zstd
import os
import pyudev


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
        archive_path (str): Path to the .tar.zst archive to decompress.
        output_path (str): Path where the decompressed folder will be created.
        level (int, optional): Compression level, defaults to 10.

    Notes:
        Extracts all files from the Zstandard-compressed TAR archive into
        the specified output directory, preserving the folder structure.
    """
    
    if not os.path.isdir(output_path):
        os.makedirs(output_path, exist_ok=True)

    tar_path = os.path.join(output_path, "tmp_extract.tar")

    dctx = zstd.ZstdDecompressor()

    with open(file_path + ".tar.zst", "rb") as input_f, open(tar_path, "wb") as output_f:
        dctx.copy_stream(input_f, output_f)

    with tarfile.open(tar_path, "r") as tf:
        tf.extractall(path=output_path, filter="data")

    os.remove(tar_path)


def get_devices_dict():
    """
    Returns a list of available external drives.

    Returns:
        list: A list of available external drives.
    """

    context = pyudev.Context()
    devices = {}
    for device in context.list_devices(subsystem="block", DEVTYPE="disk"):
        if device.get("ID_BUS") == "usb":
            with open("/proc/mounts") as f:
                for line in f:
                    if device.device_node in line:
                        devices[device.get("ID_MODEL")] = line.split()[1]
    return devices

def set_wallpaper(file_path):
    """
    Sets the desktop wallpaper to the specified image file.

    Args:
        file_path (str): Path to the image file to set as wallpaper.
    """
    if os.path.exists(file_path):
        try:
            from gi.repository import Gio
            settings = Gio.Settings("org.gnome.desktop.background")
            settings.set_string("picture-uri", f"file://{file_path}")
        except Exception as e:
            print(f"Failed to set wallpaper: {e}")
    else:
        print(f"File does not exist: {file_path}")
