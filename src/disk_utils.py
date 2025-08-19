import tarfile
import zstandard as zstd
import os
import pyudev
import shutil


def compress_folder(folder_path, output_path, level=10):
    tar_path = f"{output_path}.tar"
    zst_path = f"{output_path}.tar.zst"

    with tarfile.open(tar_path, "w:tar") as tf:
        tf.add(folder_path, arcname=".")

    compressor = zstd.ZstdCompressor(level)

    with open(tar_path, "rb") as f_in, open(zst_path, "wb") as f_out:
        compressor.copy_stream(f_in, f_out)

    os.remove(tar_path)


def decompress_folder(file_path, output_path):
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
    context = pyudev.Context()

    devices = {}

    for device in context.list_devices(subsystem="block", DEVTYPE="disk"):
        if device.get("ID_BUS") == "usb":
            with open("/proc/mounts") as f:
                for line in f:
                    if device.device_node in line:
                        devices[device.get("ID_MODEL")] = line.split()[1]

    return devices
