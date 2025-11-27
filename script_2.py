# --- Lospec Palette to OBS Theme Generation ---
import requests
from colorsys import rgb_to_hls

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def get_lightness(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = rgb_to_hls(r/255, g/255, b/255)
    return l

def get_hue(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = rgb_to_hls(r/255, g/255, b/255)
    return h

def fetch_lospec_palette(slug):
    url = f"https://lospec.com/palette-list/{slug}.json"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch palette: {slug}")
    data = resp.json()
    # Palette is a list of hex strings
    return data['colors'], data.get('title', slug)

def assign_palette_to_semantics(palette):
    """
    Assigns palette colors to Catppuccin/OBS semantic roles by analyzing lightness and hue.
    Returns a dict mapping semantic keys to hex colors.
    """
    # Catppuccin semantic keys (subset for best fit)
    semantic_keys = [
        'base', 'mantle', 'surface0', 'surface1', 'surface2',
        'text', 'subtext1', 'subtext0', 'overlay0', 'overlay1', 'overlay2',
        'red', 'maroon', 'peach', 'yellow', 'green', 'teal', 'blue', 'lavender', 'mauve', 'pink', 'flamingo', 'rosewater', 'sky', 'sapphire'
    ]
    # Sort palette by lightness
    sorted_by_lightness = sorted(palette, key=get_lightness)
    mapping = {}
    # Assign base/mantle/surface to darkest
    if len(sorted_by_lightness) >= 5:
        mapping['base'] = sorted_by_lightness[0]
        mapping['mantle'] = sorted_by_lightness[1]
        mapping['surface0'] = sorted_by_lightness[2]
        mapping['surface1'] = sorted_by_lightness[3]
        mapping['surface2'] = sorted_by_lightness[4]
    # Assign text/subtext/overlay to lightest
    if len(sorted_by_lightness) >= 8:
        mapping['text'] = sorted_by_lightness[-1]
        mapping['subtext1'] = sorted_by_lightness[-2]
        mapping['subtext0'] = sorted_by_lightness[-3]
        mapping['overlay0'] = sorted_by_lightness[-4]
        mapping['overlay1'] = sorted_by_lightness[-5]
        mapping['overlay2'] = sorted_by_lightness[-6]
    # Assign accents by hue proximity
    hue_targets = {
        'red': 0.0, 'maroon': 0.97, 'peach': 0.08, 'yellow': 0.15, 'green': 0.33, 'teal': 0.5, 'blue': 0.6, 'lavender': 0.7, 'mauve': 0.75, 'pink': 0.9, 'flamingo': 0.95, 'rosewater': 0.02, 'sky': 0.55, 'sapphire': 0.58
    }
    used = set(mapping.values())
    for key, target_hue in hue_targets.items():
        best = None
        best_dist = 2.0
        for color in palette:
            if color in used:
                continue
            hue = get_hue(color)
            dist = min(abs(hue - target_hue), 1 - abs(hue - target_hue))
            if dist < best_dist:
                best = color
                best_dist = dist
        if best:
            mapping[key] = best
            used.add(best)
    # Fill any missing keys with first unused colors
    for key in semantic_keys:
        if key not in mapping:
            for color in palette:
                if color not in used:
                    mapping[key] = color
                    used.add(color)
                    break
    return mapping

def generate_obs_theme_from_lospec(slug, output_path=None, dark_theme=True):
    palette, title = fetch_lospec_palette(slug)
    mapping = assign_palette_to_semantics(palette)
    theme_name = f"Lospec {title}"
    if not output_path:
        output_path = f"lospec_{slug}.ovt"
    # Compose OBS theme variables
    color_vars = [f"    --{k}: {v};" for k, v in mapping.items()]
    # Map semantic variables using Catppuccin mapping
    semantic_vars = []
    for obs_var, palette_key in catppuccin_semantic_mapping.items():
        hex_value = mapping.get(palette_key, '#888888')
        semantic_vars.append(f"    --{obs_var}: var(--{palette_key}, {hex_value});")
    theme_content = f"""@OBSThemeMeta {{
    name: '{theme_name}';
    id: 'com.lospec.{slug}';
    extends: 'com.obsproject.Yami';
    author: 'Generated from Lospec';
    dark: '{'true' if dark_theme else 'false'}';
}}

@OBSThemeVars {{
    /* Lospec Palette */
{chr(10).join(color_vars)}

    /* Semantic Color Variables (Catppuccin mapping) */
{chr(10).join(semantic_vars)}
}}
"""
    with open(output_path, 'w') as f:
        f.write(theme_content)
    print(f"Generated OBS theme from Lospec palette: {output_path}")

# Example usage:
# generate_obs_theme_from_lospec('1bit-monitor')

# --- New logic: TextMate-to-OBS theme conversion using Catppuccin mapping as template ---
import json
import os

def extract_palette_from_textmate(textmate_json):
    """
    Extract a palette from a TextMate theme JSON dict.
    Returns a dict of color name to hex value if possible.
    """
    # Try to extract a palette from 'colors' or 'semanticHighlighting' or similar
    palette = {}
    if 'colors' in textmate_json:
        for k, v in textmate_json['colors'].items():
            # Try to normalize keys to Catppuccin names if possible
            palette[k.lower().replace(' ', '_')] = v
    # Fallback: try to extract from tokenColors
    if not palette and 'tokenColors' in textmate_json:
        for entry in textmate_json['tokenColors']:
            if 'settings' in entry and 'foreground' in entry['settings']:
                name = entry.get('name', '').lower().replace(' ', '_')
                if name and name not in palette:
                    palette[name] = entry['settings']['foreground']
    return palette

# The official Catppuccin mapping from palette to semantic OBS variables
catppuccin_semantic_mapping = {
    'bg_window': 'base',
    'bg_base': 'mantle',
    'bg_surface': 'surface0',
    'bg_surface_raised': 'surface1',
    'bg_surface_hover': 'surface2',
    'bg_button': 'surface0',
    'bg_button_hover': 'surface1',
    'bg_button_pressed': 'surface2',
    'bg_button_checked': 'mauve',
    'bg_button_disabled': 'overlay0',
    'text_primary': 'text',
    'text_secondary': 'subtext1',
    'text_tertiary': 'subtext0',
    'text_disabled': 'overlay1',
    'text_link': 'blue',
    'text_link_hover': 'sky',
    'accent_primary': 'mauve',
    'accent_secondary': 'lavender',
    'accent_success': 'green',
    'accent_warning': 'yellow',
    'accent_error': 'red',
    'accent_info': 'blue',
    'border_base': 'overlay0',
    'border_focus': 'mauve',
    'border_hover': 'overlay1',
    'border_pressed': 'overlay2',
}

def closest_palette_color(palette, fallback='#888888'):
    # Just pick the first color in the palette, or fallback
    if palette:
        return list(palette.values())[0]
    return fallback

def generate_obs_theme_from_textmate(textmate_path, output_path, theme_name, dark_theme=True):
    with open(textmate_path, 'r') as f:
        textmate_json = json.load(f)
    palette = extract_palette_from_textmate(textmate_json)

    # Compose OBS theme variables
    color_vars = []
    for color_name, hex_value in palette.items():
        color_vars.append(f"    --{color_name}: {hex_value};")

    # Map semantic variables using Catppuccin mapping, fallback to closest color
    semantic_vars = []
    for obs_var, palette_key in catppuccin_semantic_mapping.items():
        hex_value = palette.get(palette_key, closest_palette_color(palette))
        semantic_vars.append(f"    --{obs_var}: var(--{palette_key}, {hex_value});")

    theme_content = f"""@OBSThemeMeta {{
    name: '{theme_name}';
    id: 'com.custom.{theme_name.lower().replace(' ', '_')}';
    extends: 'com.obsproject.Yami';
    author: 'Converted from TextMate';
    dark: '{'true' if dark_theme else 'false'}';
}}

@OBSThemeVars {{
    /* Extracted Palette */
{chr(10).join(color_vars)}

    /* Semantic Color Variables (Catppuccin mapping) */
{chr(10).join(semantic_vars)}
}}
"""

    with open(output_path, 'w') as f:
        f.write(theme_content)

    print(f"Generated OBS theme: {output_path}")

# Example usage:
# generate_obs_theme_from_textmate('path/to/textmate.json', 'output_theme.ovt', 'My Theme', dark_theme=True)