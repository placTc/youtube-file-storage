from qrcode import make

def generate_qr_code(data: str, destination_path: str):
    """
    Create qr code and save it

    Args:
        data (str): string to encode into a qr coee
        destination_path (str): path where we're saving the qr code
    """
    qr = make(data)
    qr.save(destination_path)
    