from pathlib import Path
from typing import Optional, Tuple
import logging
import os

logger = logging.getLogger(__name__)

class FileService:
    def __init__(self, root_path: Path):
        self.root_path = root_path.resolve()
        self.allowed_extensions = {'.ovt', '.obt', '.json'}

    def validate_and_resolve_path(self, filename: str) -> Tuple[bool, Optional[Path], str]:
        """Validate filename and return resolved path"""
        if not filename or len(filename) > 255:
            return False, None, "Invalid filename length"

        if '..' in filename or '/' in filename or '\\' in filename:
            return False, None, "Path traversal not allowed"

        clean_filename = os.path.basename(filename)
        file_path = self.root_path / clean_filename

        try:
            resolved_path = file_path.resolve()
            resolved_path.relative_to(self.root_path)
        except (ValueError, OSError):
            return False, None, "Invalid path"

        if resolved_path.suffix.lower() not in self.allowed_extensions:
            return False, None, "File type not allowed"

        return True, resolved_path, "Valid"
