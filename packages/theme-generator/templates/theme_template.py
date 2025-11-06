from typing import Dict, Any
from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path

class ThemeTemplate:
    def __init__(self, template_dir: Path):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render_theme(self,
                     theme_config: Dict[str, Any],
                     color_palette) -> str:
        """Render theme template with configuration and colors"""
        template = self.env.get_template('base_theme.ovt.j2')

        return template.render(
            config=theme_config,
            colors=color_palette.colors,
            palette_name=color_palette.name
        )
