import os
import tempfile
from disk_utils import compress_folder, decompress_folder


def test_compress_folder_creates_file():
    """Test that compress_folder creates a .tar.zst archive file from a folder."""

    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "data")
        os.mkdir(input_dir)

        test_file = os.path.join(input_dir, "hello.txt")
        with open(test_file, "w") as f:
            f.write("helo12345")

        output_path = os.path.join(tmpdir, "archive")
        compress_folder(input_dir, output_path)

        archive_file = f"{output_path}.tar.zst"
        assert os.path.exists(archive_file), f"Archive {archive_file} was not created."


def test_decompress_folder_decompress_files():
    """Test that decompress_folder properly extracts files from a compressed archive."""

    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "data")
        os.mkdir(input_dir)

        test_file = os.path.join(input_dir, "hello.txt")
        with open(test_file, "w") as f:
            f.write("helo12345")

        output_path = os.path.join(tmpdir, "archive")
        compress_folder(input_dir, output_path)

        decompress_dir = os.path.join(tmpdir, "decompressed")
        os.mkdir(decompress_dir)

        decompress_folder(output_path, decompress_dir)

        files = os.listdir(decompress_dir)
        assert (
            "hello.txt" in files
        ), f"'hello.txt' not found after decompression in {decompress_dir}"
