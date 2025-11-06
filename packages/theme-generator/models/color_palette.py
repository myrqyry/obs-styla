from dataclasses import dataclass
from typing import Dict, Optional
import re

@dataclass
class ColorPalette:
    name: str
    colors: Dict[str, str]

    def __post_init__(self):
        self._validate_colors()

    def _validate_colors(self):
        """Validate that all colors are valid hex codes"""
        hex_pattern = re.compile(r'^#[0-9a-fA-F]{6}$')
        for name, color in self.colors.items():
            if not hex_pattern.match(color):
                raise ValueError(f"Invalid hex color '{color}' for '{name}'")

    def get_color(self, name: str, fallback: Optional[str] = None) -> str:
        """Get color with optional fallback"""
        return self.colors.get(name, fallback or "#000000")
