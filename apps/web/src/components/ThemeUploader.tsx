import React, { useContext } from 'react';
import { ThemeContext } from '../context/ThemeContext';

const vscodeToOBSMapping: { [key: string]: string } = {
  // Core UI
  'editor.background': 'ui_background',
  'editor.foreground': 'ui_text',
  'activityBar.background': 'dock_background',
  'sideBar.background': 'dock_background',
  'sideBar.foreground': 'ui_text',
  'sideBar.border': 'ui_border',
  'titleBar.activeBackground': 'header_background',
  'titleBar.activeForeground': 'ui_text',
  'titleBar.inactiveBackground': 'header_background',

  // Interactive Elements
  'focusBorder': 'accent',

  // Components
  'button.background': 'button_background',
  'button.foreground': 'button_text',
  'button.hoverBackground': 'button_background_hover',

  'input.background': 'input_background',
  'input.foreground': 'input_text',
  'input.border': 'input_border',
  'inputOption.activeBorder': 'accent',

  'list.activeSelectionBackground': 'list_active_selection_background',
  'list.activeSelectionForeground': 'list_active_selection_text',
  'list.hoverBackground': 'list_hover_background',
  'list.focusBackground': 'list_active_selection_background',

  'scrollbar.shadow': 'ui_background_dark',
  'scrollbarSlider.background': 'scrollbar_handle',
  'scrollbarSlider.hoverBackground': 'scrollbar_handle_hover',
  'scrollbarSlider.activeBackground': 'scrollbar_handle_hover',

  // OBS-Specific & Status Bar
  'statusBar.background': 'statusbar_background',
  'statusBar.foreground': 'statusbar_text',
  'statusBar.noFolderBackground': 'statusbar_background',

  // Semantic Colors
  'editorError.foreground': 'error',
  'editorWarning.foreground': 'warning',
  'editorInfo.foreground': 'info',

  // Syntax/Editor
  'editor.selectionBackground': 'list_active_selection_background',
  'editorLineNumber.foreground': 'ui_text_dark',
  'editorLineNumber.activeForeground': 'accent',

  // Tabs
  'tab.activeBackground': 'tab_active_background',
  'tab.inactiveBackground': 'tab_background',
  'tab.activeForeground': 'tab_active_text',
  'tab.inactiveForeground': 'tab_text',
  'tab.border': 'ui_border',

  // Tooltip & Menu
  'editor.hoverHighlightBackground': 'tooltip_background',
  'menu.background': 'menu_background',
  'menu.foreground': 'menu_text',
  'menu.selectionBackground': 'menu_selection_background',
};

const ThemeUploader = () => {
  const { dispatch } = useContext(ThemeContext);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const text = e.target?.result as string;
          const themeJSON = JSON.parse(text);
          parseAndApplyTheme(themeJSON);
        } catch (error) {
          console.error('Error parsing theme file:', error);
          // Handle parsing error (e.g., show a notification)
        }
      };
      reader.readAsText(file);
    }
  };

  const parseAndApplyTheme = (themeJSON: any) => {
    if (themeJSON.colors && typeof themeJSON.colors === 'object') {
      Object.entries(vscodeToOBSMapping).forEach(([vscodeKey, obsKey]) => {
        if (themeJSON.colors[vscodeKey]) {
          dispatch({
            type: 'SET_COLOR',
            payload: { key: obsKey as any, value: themeJSON.colors[vscodeKey] },
          });
        }
      });
    }
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Import VSCode Theme</h3>
      <input
        type="file"
        accept=".json"
        onChange={handleFileChange}
        className="block w-full text-sm text-foreground file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-primary-foreground hover:file:bg-primary/90"
      />
    </div>
  );
};

export default ThemeUploader;
