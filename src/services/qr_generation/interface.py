"""QR Code generator interface"""

from pathlib import Path
from typing import Callable, Sequence

QRGenerator = Callable[[Sequence, Path | str], None]
StringQRGenerator = Callable[[str, Path | str], None]
BinaryQRGenerator = Callable[[bytes, Path | str], None]