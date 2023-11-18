from functools import partial
from io import BytesIO, StringIO
from pathlib import Path
from base64io import Base64IO


def base64_converter_factory(temporary_file_path: Path | str, processing_chunk_size: int = 1024):
    """
    Return a partial base64 encoder function with the temp file and processing chunk size fields already filled in

    Args:
        temporary_file_path (Path | str): _description_
        processing_chunk_size (int, optional): _description_. Defaults to 1024.

    Returns:
        _type_: _description_
    """
    return partial(
        base64_converter, temporary_file_path=temporary_file_path, processing_chunk_size=processing_chunk_size
    )


def base64_converter(
    source_buffer: BytesIO, temporary_file_path: Path | str, processing_chunk_size: int = 1024
) -> StringIO:
    """
    Convert a source buffer into a base64 string and return a file containing the resulting string

    Args:
        source_buffer (BytesIO): Buffer to read from
        temporary_file_path (Path | str): THe path to the file we're writing the base64 data into
        processing_chunk_size (int, optional): The chunk size to use when reading from the source buffier. Defaults to 1024.

    Returns:
        StringIO: _description_
    """
    with open(temporary_file_path, "wb") as output_file:
        _write_base64_encoded_data(source_buffer, output_file, processing_chunk_size)

    return open(temporary_file_path, "r")


def _write_base64_encoded_data(source_buffer: BytesIO, target_buffer: BytesIO, chunk_size: int):
    """
    Writes data into buffer, automatically encoding it into Base64

    Args:
        source_buffer (BytesIO): Buffer to read from
        target_buffer (BytesIO): Buffer to write into
        chunk_size (int): Chunk size of bytes to read from the source buffer, -1 indicates to read all of the data
    """

    with Base64IO(target_buffer) as base64_encoder_buffer:
        _write_into_buffer(source_buffer, base64_encoder_buffer, chunk_size)


def _write_into_buffer(source_buffer: BytesIO, target_buffer: BytesIO, chunk_size: int):
    """
    Writes data from binary buffer into another binary buffer

    Args:
        source_buffer (BytesIO): Buffer to read from
        target_buffer (BytesIO): Buffer to write into
        chunk_size (int): Chunk size of bytes to read from the source buffer, -1 indicates to read all of the data
    """
    while True:
        chunk = source_buffer.read(chunk_size)
        if not chunk:
            break

        target_buffer.write(chunk)
