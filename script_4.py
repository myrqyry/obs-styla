# Create a new OBS theme based on the Dracula color palette.
# This will be a complete .ovt theme file compatible with OBS Studio 30.2+

dracula_colors = {
    "background": "#282a36",
    "current_line": "#44475a",
    "foreground": "#f8f8f2",
    "comment": "#6272a4",
    "cyan": "#8be9fd",
    "green": "#50fa7b",
    "orange": "#ffb86c",
    "pink": "#ff79c6",
    "purple": "#bd93f9",
    "red": "#ff5555",
    "yellow": "#f1fa8c"
}

with open('dracula_theme.template.ovt', 'r') as f:
    template_content = f.read()

theme_content = template_content.format(**dracula_colors)

with open('dracula_theme.ovt', 'w') as f:
    f.write(theme_content)

print("✅ Theme saved as 'dracula_theme.ovt'")
