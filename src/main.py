# BIG THINGS UNDERWAY !!!

from tempfile import TemporaryDirectory

from pathlib import Path
from services.conversion import base64_converter_factory
from services.qr_generation.qrcode_library_generator import qr_code_generator_factory
from services.qr_generation.text_file_into_qr_codes import convert_file_into_qr_codes
from services.temporary_file.temporary_file import create_temporary_file
from services.qr_generation.constants import MAX_SIZE_FOR_EC_LEVEL, LOW_ERROR_CORRECTION

TEST_FILE = r"C:\Users\plasm\Desktop\map.png"


with TemporaryDirectory() as main_temp_dir:
    with create_temporary_file(Path(main_temp_dir)) as temporary_file_path:
        base64_converter = base64_converter_factory(temporary_file_path)
        with open(TEST_FILE, "rb") as source_file:
            encoded_file = base64_converter(source_file)

        qr_generator = qr_code_generator_factory(LOW_ERROR_CORRECTION)
        with TemporaryDirectory() as qr_codes_dir:
            convert_file_into_qr_codes(encoded_file, qr_codes_dir, qr_generator, MAX_SIZE_FOR_EC_LEVEL[LOW_ERROR_CORRECTION])
            print("done!")
            