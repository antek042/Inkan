import tarfile
import zstandard as zstd

def compress_folder(folder_path, output_path, level=10):
    tar_path = f"{output_path}.tar.gz"
    zst_path = f"{output_path}.tar.gz.zst"

    with tarfile.open(tar_path, "w|gz") as tf:
        tf.add(folder_path, arcname=".")
    compressor = zstd.ZstdCompressor(level)
    with open(tar_path, "rb") as f_in, open(zst_path, "wb") as f_out:
        compressor.copy_stream(f_in, f_out)
    