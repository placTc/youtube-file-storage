from contextlib import contextmanager
import os
from typing import ContextManager

from pathlib import Path
from uuid import uuid4


@contextmanager
def create_temporary_file(dir: Path) -> ContextManager[Path]:
    """
    Context manager to create a file and remove it after
    
    Args:
        path (str | Path): Path to directory where file will be stored
    """
    
    filename = str(uuid4())
    try:
        file = open(dir / filename, "wb")
        file.close()
        yield dir / filename
    finally:
        os.remove(dir / filename)
    