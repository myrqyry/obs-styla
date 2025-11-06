import logging
from pathlib import Path
from typing import Dict, Any, Optional
from ..models.color_palette import ColorPalette
from ..templates.theme_template import ThemeTemplate
import re

logger = logging.getLogger(__name__)

class ThemeGenerationError(Exception):
    """Raised when theme generation fails"""
    pass

class ThemeGenerator:
    def __init__(self, output_dir: Path, template_dir: Path):
        self.output_dir = output_dir
        self.template_engine = ThemeTemplate(template_dir)

    def generate_theme(self,
                       config: Dict[str, Any],
                       palette: ColorPalette,
                       output_filename: Optional[str] = None) -> Path:
        """Generate a theme file from configuration and color palette"""
        try:
            # Validate configuration
            self._validate_config(config)

            # Generate theme content
            theme_content = self.template_engine.render_theme(config, palette)

            # Determine output filename
            if not output_filename:
                safe_name = config['name'].replace(' ', '_').lower()
                output_filename = f"{safe_name}.ovt"

            output_path = self.output_dir / output_filename

            # Write theme file
            output_path.write_text(theme_content, encoding='utf-8')

            logger.info(f"Generated theme: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Theme generation failed: {e}")
            raise ThemeGenerationError(f"Failed to generate theme: {e}") from e

    def _validate_config(self, config: Dict[str, Any]):
        """Validate theme configuration"""
        required_fields = ['name', 'id', 'author']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")

        if not config['name'].strip():
            raise ValueError("Theme name cannot be empty")

        # Validate theme ID format
        if not re.match(r'^[a-z0-9._-]+$', config['id']):
            raise ValueError("Theme ID must contain only lowercase letters, numbers, dots, and hyphens")
