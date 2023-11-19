"""
Alphanumeric converter interface
"""

from io import BytesIO, StringIO
from typing import Callable

# Converter function signature
Converter = Callable[[BytesIO], StringIO]
