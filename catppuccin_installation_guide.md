# Catppuccin Enhanced Theme Collection for OBS Studio

## Overview
This collection provides all four authentic Catppuccin flavors (Latte, Frappé, Macchiato, Mocha) as enhanced OBS Studio themes, fully compatible with OBS 30.2+ and the new composable theme system.

## Installation Guide

### Step 1: Locate Your OBS Themes Directory
- **Windows**: `%APPDATA%\obs-studio\themes\`
- **macOS**: `~/Library/Application Support/obs-studio/themes/`
- **Linux**: `~/.config/obs-studio/themes/`

### Step 2: Install Theme Files
1. Copy the desired `.ovt` files to your themes directory
2. If the themes directory doesn't exist, create it manually
3. Restart OBS Studio

### Step 3: Apply Theme
1. Open OBS Studio
2. Go to **File > Settings** (or **OBS > Preferences** on macOS)
3. Navigate to **Appearance** tab
4. Select "Catppuccin Enhanced [Flavor]" from the **Theme** dropdown
5. Click **Apply** and **OK**

## Available Themes

### 🌻 Latte (Light Theme)
- **File**: `catppuccin_enhanced_latte.ovt`
- **Best for**: Daytime streaming, bright environments
- **Colors**: Warm, light pastel palette

### 🪴 Frappé (Dark Theme)
- **File**: `catppuccin_enhanced_frappe.ovt`
- **Best for**: Evening streaming, medium contrast
- **Colors**: Cool, muted dark palette

### 🌺 Macchiato (Dark Theme)
- **File**: `catppuccin_enhanced_macchiato.ovt`
- **Best for**: Night streaming, balanced contrast
- **Colors**: Warm, medium dark palette

### 🌿 Mocha (Dark Theme)
- **File**: `catppuccin_enhanced_mocha.ovt`
- **Best for**: Late night streaming, high contrast
- **Colors**: Deep, rich dark palette

## Troubleshooting

### Theme Not Showing Up
1. Ensure you're using OBS Studio 30.2 or later
2. Check that files are in the correct themes directory
3. Restart OBS Studio completely
4. Verify file permissions (should be readable)

### Theme Appears Broken
1. Ensure you have the latest version of OBS Studio
2. Try selecting "Yami" theme first, then switch to Catppuccin
3. Check OBS logs for theme-related errors

### Colors Look Wrong
1. Verify your display color profile settings
2. Check monitor calibration
3. Ensure HDR is properly configured if enabled

## Features

### Enhanced UI Elements
- Smooth hover transitions
- Contextual button colors
- Improved contrast ratios
- Consistent spacing and typography
- Modern border radius and shadows

### OBS-Specific Styling
- Color-coded recording/streaming buttons
- Enhanced volume meter colors
- Improved source/scene list styling
- Better dock and splitter appearance
- Optimized settings panel layout

### Accessibility
- WCAG compliant contrast ratios
- Clear focus indicators
- Consistent interactive feedback
- Readable text at all sizes

## Customization

These themes use CSS variables for easy customization. Advanced users can modify:
- Color values in the `@OBSThemeVars` section
- Border radius and spacing values
- Animation timing and effects
- Component-specific styling

## Support

For issues or questions:
1. Check OBS Studio logs for errors
2. Verify theme file integrity
3. Test with default themes first
4. Report bugs with system information and OBS version

## Credits
- **Catppuccin**: Original color palette by @catppuccin
- **OBS Studio**: Open-source streaming software
- **Enhanced Themes**: Created with AI assistance for OBS 32 compatibility
