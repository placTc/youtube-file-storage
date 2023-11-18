from functools import partial
from qrcode import make
from services.qr_generation.constants import LOW_ERROR_CORRECTION
from services.qr_generation.interface import QRGenerator



def qr_code_generator_factory(error_correction_value: int = LOW_ERROR_CORRECTION) -> QRGenerator:
    """
    Factory that creates a qr generator with a set error correction level

    Args:
        error_correction_value (int, optional): Error correction level to use. Defaults to 0.

    Returns:
        QRGenerator: function that creates qr codes
    """
    return partial(generate_qr_code, error_correction=error_correction_value)


def generate_qr_code(data: str, destination_path: str, error_correction: int = LOW_ERROR_CORRECTION):
    """
    Create qr code and save it

    Args:
        data (str): string to encode into a qr coee
        destination_path (str): path where we're saving the qr code
        error_correction (int): error correction level. Defaults to 0
            0 - Low: 7% of bytes can be restored
            1 - Medium: 15% of bytes can be restored
            2 - Quartile: 25% of bytes can be restored
            3 - High: 30% of bytes can be restored
    """
    true_ec_value = _convert_error_correction_value(error_correction)
    qr = make(data)
    qr.save(destination_path, error_correction=true_ec_value)

def _convert_error_correction_value(error_correction: int) -> int:
    if error_correction in [1, 3]:
        return error_correction - 1
    
    return error_correction + 1