#!/usr/bin/env node

// Batch script to generate multiple OBS themes from popular TextMate themes
// Usage: node generate_popular_themes.js

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Popular themes to generate
const popularThemes = [
    'dracula',
    'github-dark',
    'github-light',
    'material-theme',
    'material-theme-darker',
    'material-theme-lighter',
    'material-theme-ocean',
    'material-theme-palenight',
    'nord',
    'one-dark-pro',
    'palenight-theme',
    'solarized-dark',
    'solarized-light',
    'tokyo-night',
    'tokyo-night-storm',
    'vscode-dark-modern',
    'vscode-light-modern'
];

// Map TextMate color tokens to OBS theme colors
function mapTextMateToObsColors(themeColors) {
    return {
        background: themeColors['editor.background'] || themeColors['background'] || '#282a36',
        current_line: themeColors['editor.selectionBackground'] || themeColors['selection.background'] || '#44475a',
        foreground: themeColors['editor.foreground'] || themeColors['foreground'] || '#f8f8f2',
        comment: themeColors['editorLineNumber.foreground'] || themeColors['comments'] || '#6272a4',
        cyan: themeColors['editorInfo.foreground'] || themeColors['editor.infoForeground'] || '#8be9fd',
        green: themeColors['editorGutter.addedBackground'] || '#50fa7b',
        orange: themeColors['editorWarning.foreground'] || themeColors['editor.warningForeground'] || '#ffb86c',
        pink: themeColors['editorGutter.modifiedBackground'] || '#ff79c6',
        purple: themeColors['editorGutter.deletedBackground'] || '#bd93f9',
        red: themeColors['editorError.foreground'] || themeColors['editor.errorForeground'] || '#ff5555',
        yellow: themeColors['editorWarning.foreground'] || '#f1fa8c'
    };
}

// Generate OBS theme content
function generateObsTheme(themeName, displayName, colors) {
    const obsColors = mapTextMateToObsColors(colors);

    return `@OBSThemeMeta {{
    name: '${displayName}';
    id: 'com.textmate.${themeName.toLowerCase().replace(/[^a-z0-9]/g, '')}.theme';
    extends: 'com.obsproject.Yami';
    author: 'TextMate Theme';
    dark: 'true';
}}

@OBSThemeVars {{
    /* ${displayName} Color Palette */
    --background: ${obsColors.background};
    --current_line: ${obsColors.current_line};
    --foreground: ${obsColors.foreground};
    --comment: ${obsColors.comment};
    --cyan: ${obsColors.cyan};
    --green: ${obsColors.green};
    --orange: ${obsColors.orange};
    --pink: ${obsColors.pink};
    --purple: ${obsColors.purple};
    --red: ${obsColors.red};
    --yellow: ${obsColors.yellow};

    /* Semantic Color Variables */
    --bg_window: var(--background);
    --bg_base: var(--current_line);
    --bg_surface: #3a3c4e;
    --bg_surface_raised: #4e5066;
    --bg_surface_hover: #5a5c72;
    --bg_button: var(--current_line);
    --bg_button_hover: #5a5c72;
    --bg_button_pressed: #6b6d80;
    --bg_button_checked: var(--purple);
    --bg_button_disabled: var(--comment);

    /* Text Colors */
    --text_primary: var(--foreground);
    --text_secondary: #e0e0e0;
    --text_tertiary: #c0c0c0;
    --text_disabled: var(--comment);
    --text_link: var(--cyan);
    --text_link_hover: #a0ffff;

    /* Accent Colors */
    --accent_primary: var(--purple);
    --accent_secondary: var(--pink);
    --accent_success: var(--green);
    --accent_warning: var(--orange);
    --accent_error: var(--red);
    --accent_info: var(--cyan);

    /* Border Colors */
    --border_base: var(--comment);
    --border_focus: var(--purple);
    --border_hover: #7a88b8;
    --border_pressed: #8a98c8;

    /* Sizing Variables */
    --border_radius: 8px;
    --border_radius_small: 4px;
    --border_radius_large: 12px;
    --spacing_xs: 4px;
    --spacing_sm: 8px;
    --spacing_md: 12px;
    --spacing_lg: 16px;
    --spacing_xl: 24px;

    /* Animation Variables */
    --transition_fast: 150ms;
    --transition_normal: 250ms;
    --transition_slow: 350ms;
}}

/* Main Application Window */
QMainWindow {{
    background-color: var(--bg_window);
    color: var(--text_primary);
}}

/* Dock Areas and Splitters */
QDockWidget {{
    background-color: var(--bg_base);
    color: var(--text_primary);
    border: 1px solid var(--border_base);
    border-radius: var(--border_radius);
}}

QDockWidget::title {{
    background-color: var(--bg_surface);
    padding: var(--spacing_sm);
    border-bottom: 1px solid var(--border_base);
    font-weight: 600;
}}

QSplitter::handle {{
    background-color: var(--border_base);
}}

QSplitter::handle:horizontal {{
    width: 2px;
}}

QSplitter::handle:vertical {{
    height: 2px;
}}

/* Buttons */
QPushButton {{
    background-color: var(--bg_button);
    color: var(--text_primary);
    border: 1px solid var(--border_base);
    border-radius: var(--border_radius);
    padding: var(--spacing_sm) var(--spacing_md);
    font-weight: 500;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: var(--bg_button_hover);
    border-color: var(--border_hover);
}}

QPushButton:pressed {{
    background-color: var(--bg_button_pressed);
    border-color: var(--border_pressed);
}}

QPushButton:checked {{
    background-color: var(--bg_button_checked);
    color: var(--foreground);
    border-color: var(--accent_primary);
}}

QPushButton:disabled {{
    background-color: var(--bg_button_disabled);
    color: var(--text_disabled);
    border-color: var(--border_base);
}}`;
}

// Main function
async function main() {
    console.log('🎨 Generating popular OBS themes from TextMate...\n');

    let successCount = 0;
    let failCount = 0;

    for (const themeName of popularThemes) {
        try {
            // Import the specific theme
            const themePath = `tm-themes/themes/${themeName}.json`;
            const theme = await import(themePath, { with: { type: 'json' } });

            const obsTheme = generateObsTheme(themeName, theme.default.displayName || themeName, theme.default.colors);

            // Write to file in parent directory (root of monorepo)
            const outputFile = path.join(__dirname, '..', '..', `${themeName}_theme.ovt`);
            fs.writeFileSync(outputFile, obsTheme);

            console.log(`✅ ${theme.default.displayName || themeName} (${Object.keys(theme.default.colors).length} colors)`);
            successCount++;

        } catch (error) {
            console.log(`❌ ${themeName}: ${error.message}`);
            failCount++;
        }
    }

    console.log(`\n🎉 Generated ${successCount} themes successfully${failCount > 0 ? `, ${failCount} failed` : ''}`);
    console.log('📁 Themes saved to root directory');
}

main().catch(console.error);