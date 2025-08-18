import tarfile
import zstandard as zstd
import os
import pyudev

def compress_folder(folder_path, output_path, level=10):
    tar_path = f"{output_path}.tar.gz"
    zst_path = f"{output_path}.tar.gz.zst"

    with tarfile.open(tar_path, "w|gz") as tf:
        tf.add(folder_path, arcname=".")
    compressor = zstd.ZstdCompressor(level)
    with open(tar_path, "rb") as f_in, open(zst_path, "wb") as f_out:
        compressor.copy_stream(f_in, f_out)
    os.remove(tar_path)

def decompress_folder(folder_path, output_path, level=10):
    tar_path = f"{output_path}.tar.gz"
    zst_path = f"{folder_path}.tar.gz.zst"

    decompressor = zstd.ZstdDecompressor()
    with open(zst_path, "rb") as input, open(tar_path, "wb") as output:
        decompressor.copy_stream(input, output)
    with tarfile.open(tar_path, "r|gz") as tf:
        tf.extractall(path=".",filter="data")
    os.remove(tar_path)

def get_devices_dict():
    context = pyudev.Context()
    devices = {}
    for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
        if device.get("ID_BUS") == "usb":
            with open("/proc/mounts") as f:
                for line in f:
                    if device.device_node in line:
                        devices[device.get("ID_MODEL")] = line.split()[1]
    return devices
