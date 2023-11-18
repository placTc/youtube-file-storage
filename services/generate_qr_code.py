from qrcode import make

def generate_qr_code(data: str, filename: str):
    qr = make(data)
    qr.save(filename)
    