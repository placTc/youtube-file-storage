"""QR Code generator interface"""

from pathlib import Path
from typing import Callable


QRGenerator = Callable[[str, Path | str]]