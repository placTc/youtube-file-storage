from tempfile import TemporaryFile
from uuid import uuid4
from qrcodegen import *
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def generate_qr_code(data: bytes, destination_path: str):
    qr = QrCode.encode_binary(data, QrCode.Ecc.LOW)
    svg = to_svg_str(qr, 4)
    tempfile_name = str(uuid4())
    with open(tempfile_name, "w") as temp:
        temp.write(svg)
    
    drawing = svg2rlg(temp.name)
    renderPM.drawToFile(drawing, destination_path)
        
    
    
    
def to_svg_str(qr: QrCode, border: int) -> str:
	"""Returns a string of SVG code for an image depicting the given QR Code, with the given number
	of border modules. The string always uses Unix newlines (\n), regardless of the platform."""
	if border < 0:
		raise ValueError("Border must be non-negative")
	parts: List[str] = []
	for y in range(qr.get_size()):
		for x in range(qr.get_size()):
			if qr.get_module(x, y):
				parts.append(f"M{x+border},{y+border}h1v1h-1z")
	return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 {qr.get_size()+border*2} {qr.get_size()+border*2}" stroke="none">
	<rect width="100%" height="100%" fill="#FFFFFF"/>
	<path d="{" ".join(parts)}" fill="#000000"/>
</svg>
"""