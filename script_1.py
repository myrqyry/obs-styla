import json
from pathlib import Path
from packages.theme-generator.generators.theme_generator import ThemeGenerator, ThemeGenerationError
from packages.theme-generator.models.color_palette import ColorPalette

# Load color palette
catppuccin_mocha = ColorPalette(
    name="Catppuccin Mocha",
    colors={
        "rosewater": "#f4dbd6",
        "flamingo": "#f0c6c6",
        "pink": "#f5bde6",
        "mauve": "#c6a0f6",
        "red": "#ed8796",
        "maroon": "#ee99a0",
        "peach": "#f5a97f",
        "yellow": "#eed49f",
        "green": "#a6da95",
        "teal": "#8bd5ca",
        "sky": "#91d7e3",
        "sapphire": "#7dc4e4",
        "blue": "#8aadf4",
        "lavender": "#b7bdf8",
        "text": "#cad3f5",
        "subtext1": "#b8c0e0",
        "subtext0": "#a5adcb",
        "overlay2": "#939ab7",
        "overlay1": "#8087a2",
        "overlay0": "#6e738d",
        "surface2": "#5b6078",
        "surface1": "#494d64",
        "surface0": "#363a4f",
        "base": "#24273a",
        "mantle": "#1e2030",
        "crust": "#181926",
    }
)

# Theme configuration
config = {
    "name": "Catppuccin Enhanced",
    "id": "com.catppuccin.enhanced.mocha",
    "extends": "com.obsproject.Yami",
    "author": "Enhanced by AI Assistant",
    "dark": True
}

# Generate theme
generator = ThemeGenerator(
    output_dir=Path.cwd(),
    template_dir=Path(__file__).parent / "packages/theme-generator/templates"
)

try:
    output_path = generator.generate_theme(config, catppuccin_mocha)
    print(f"✅ Theme generated successfully: {output_path}")
except ThemeGenerationError as e:
    print(f"❌ Generation failed: {e}")
    exit(1)
