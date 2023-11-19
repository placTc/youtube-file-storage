from asyncio import as_completed
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
import math
import os
from typing import IO, Generator
from tqdm import tqdm

from click import Path
from typing import Any

from services.qr_generation.interface import QRGenerator
from services.qr_generation.constants import MEDIUM_ERROR_CORRECTION_MAX_DATA_SIZE
from multipledispatch import dispatch


def _create_qr(target_folder: str, filename: Any, part: str, qr_generator: QRGenerator, progress_bar: tqdm):
    target_path = _create_target_path(target_folder, f"{filename}.png")
    qr_generator(part, target_path)
    progress_bar.update(1)
    

def convert_file_into_qr_codes(text_file: IO, target_folder: Path | str, qr_generator: QRGenerator, qr_data_size: int = MEDIUM_ERROR_CORRECTION_MAX_DATA_SIZE):
    """
    Take a text file buffer and convert it into multiple qr images inside a folder

    Args:
        text_file (StringIO): File object to read from
        target_folder (Path | str): Folder to save the qrs into
        qr_generator (QRGenerator): QR generator function
        qr_data_size (int, optional): Amount of data to store in each qr code. Defaults to 2331 (QR size for medium error correction).
    """
    
    filesize = os.fstat(text_file.fileno()).st_size
    number_of_qrs = math.ceil(filesize / qr_data_size)
    
    print(f"File size in bytes: {filesize}")
    print(f"Number of QRs to be generated: {number_of_qrs}")
    
    
    with tqdm(total=number_of_qrs) as progress_bar:
        with ThreadPoolExecutor(max_workers=32) as executor:
            for index, part in _part_generator(text_file, qr_data_size):
                executor.submit(_create_qr, target_folder, index, part, qr_generator, progress_bar) 
        
        
@dispatch(str, str)
def _create_target_path(path: str, file: str) -> Path:
    truncated_path = path
    path_comparison_var = truncated_path
    while True:
        truncated_path = truncated_path.removesuffix("/").removesuffix("\\")
        if truncated_path == path_comparison_var:
            break
        path_comparison_var = truncated_path
    if os.name == "nt":
        return truncated_path + "\\" + file
    
    return truncated_path + "/" + file
        


@dispatch(Path, str)
def _create_target_path(path: Path, file: str) -> Path:
    return path / file


def _part_generator(text_file: StringIO, qr_data_size: int) -> Generator[str, None, None]:
    index = 0
    while True:
        part = text_file.read(qr_data_size)
        if not part:
            break
        
        yield index, part
        index += 1
        
    return None

        
