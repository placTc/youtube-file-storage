from io import StringIO

from click import Path

from services.qr_generation.interface import QRGenerator
from services.qr_generation.constants import MEDIUM_ERROR_CORRECTION_MAX_DATA_SIZE

def convert_text_file_into_qr_codes(text_file: StringIO, target_folder: Path | str, qr_generator: QRGenerator, qr_data_size: int = MEDIUM_ERROR_CORRECTION_MAX_DATA_SIZE):
    """
    Take a text file buffer and convert it into multiple qr images inside a folder

    Args:
        text_file (StringIO): File object to read from
        target_folder (Path | str): Folder to save the qrs into
        qr_generator (QRGenerator): QR generator function
        qr_data_size (int, optional): Amount of data to store in each qr code. Defaults to 2331 (QR size for medium error correction).
    """
    index = 0
    while True:
        part = text_file.read(qr_data_size)
        if not part:
            break
        
        qr_generator(part, target_folder / f"{index}.png")
        
        
