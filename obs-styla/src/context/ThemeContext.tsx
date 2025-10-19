import React, { createContext, useReducer, Dispatch, ReactNode } from 'react';

// 1. Define the state shape based on themeSchema
interface ThemeMetadata {
  name: string;
  id: string;
  extends: string;
  author: string;
  dark: boolean;
}

interface ThemeColors {
  // Core UI
  ui_background: string;
  ui_background_dark: string;
  ui_background_light: string;
  ui_text: string;
  ui_text_dark: string;
  ui_text_light: string;
  ui_border: string;

  // Interactive Elements
  accent: string;
  accent_hover: string;
  accent_text: string;

  // Components
  button_background: string;
  button_background_hover: string;
  button_text: string;

  input_background: string;
  input_text: string;
  input_border: string;
  input_border_focus: string;

  list_background: string;
  list_text: string;
  list_hover_background: string;
  list_active_selection_background: string;
  list_active_selection_text: string;

  scrollbar_background: string;
  scrollbar_handle: string;
  scrollbar_handle_hover: string;

  // OBS-Specific
  header_background: string;
  dock_background: string;

  statusbar_background: string;
  statusbar_text: string;

  volumemeter_background: string;
  volumemeter_good: string;
  volumemeter_warning: string;
  volumemeter_peak: string;

  // Semantic Colors
  success: string;
  warning: string;
  error: string;
  info: string;

  // Syntax/Editor (from VSCode import)
  syntax_keyword: string;
  syntax_string: string;
  syntax_number: string;
  syntax_comment: string;

  // Tabs
  tab_background: string;
  tab_active_background: string;
  tab_text: string;
  tab_active_text: string;

  tooltip_background: string;
  tooltip_text: string;

  menu_background: string;
  menu_text: string;
  menu_selection_background: string;
}


interface ThemeTypography {
  // Define typography properties here
}

interface ThemeLayout {
  // Define layout properties here
}

export interface ThemeState {
  metadata: ThemeMetadata;
  colors: ThemeColors;
  typography: ThemeTypography;
  layout: ThemeLayout;
}

// 2. Define the initial state
export const initialState: ThemeState = {
  metadata: {
    name: 'Default Theme',
    id: 'com.example.default-theme',
    extends: 'com.obsproject.Yami',
    author: 'obs-styla',
    dark: true,
  },
  colors: {
    // Core UI
    ui_background: '#1e1e2e',
    ui_background_dark: '#181825',
    ui_background_light: '#2a2f42',
    ui_text: '#cdd6f4',
    ui_text_dark: '#a6adc8',
    ui_text_light: '#bac2de',
    ui_border: '#494d64',
    // Interactive Elements
    accent: '#89b4fa',
    accent_hover: '#a6caff',
    accent_text: '#1e1e2e',
    // Components
    button_background: '#363a4f',
    button_background_hover: '#4a5060',
    button_text: '#cdd6f4',
    input_background: '#363a4f',
    input_text: '#cdd6f4',
    input_border: '#494d64',
    input_border_focus: '#89b4fa',
    list_background: '#1e1e2e',
    list_text: '#cdd6f4',
    list_hover_background: '#363a4f',
    list_active_selection_background: '#494d64',
    list_active_selection_text: '#cdd6f4',
    scrollbar_background: '#181825',
    scrollbar_handle: '#363a4f',
    scrollbar_handle_hover: '#4a5060',
    // OBS-Specific
    header_background: '#1e1e2e',
    dock_background: '#181825',
    statusbar_background: '#1e1e2e',
    statusbar_text: '#cdd6f4',
    volumemeter_background: '#181825',
    volumemeter_good: '#a6e3a1',
    volumemeter_warning: '#f9e2af',
    volumemeter_peak: '#f38ba8',
    // Semantic Colors
    success: '#a6e3a1',
    warning: '#f9e2af',
    error: '#f38ba8',
    info: '#89b4fa',
    // Syntax/Editor
    syntax_keyword: '#cba6f7',
    syntax_string: '#a6e3a1',
    syntax_number: '#fab387',
    syntax_comment: '#7f849c',
    // Tabs
    tab_background: '#1e1e2e',
    tab_active_background: '#363a4f',
    tab_text: '#a6adc8',
    tab_active_text: '#cdd6f4',
    tooltip_background: '#363a4f',
    tooltip_text: '#cdd6f4',
    menu_background: '#1e1e2e',
    menu_text: '#cdd6f4',
    menu_selection_background: '#363a4f',
  },
  typography: {},
  layout: {},
};

// 3. Define actions
type Action =
  | { type: 'SET_METADATA'; payload: Partial<ThemeMetadata> }
  | { type: 'SET_COLOR'; payload: { key: keyof ThemeColors; value: string } };

// 4. Create the reducer function
const themeReducer = (state: ThemeState, action: Action): ThemeState => {
  switch (action.type) {
    case 'SET_METADATA':
      return {
        ...state,
        metadata: { ...state.metadata, ...action.payload },
      };
    case 'SET_COLOR':
      return {
        ...state,
        colors: { ...state.colors, [action.payload.key]: action.payload.value },
      };
    default:
      return state;
  }
};

// 5. Create the context
interface ThemeContextProps {
  state: ThemeState;
  dispatch: Dispatch<Action>;
}

export const ThemeContext = createContext<ThemeContextProps>({
  state: initialState,
  dispatch: () => null,
});

// 6. Create the ThemeProvider component
interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider = ({ children }: ThemeProviderProps) => {
  const [state, dispatch] = useReducer(themeReducer, initialState);

  return (
    <ThemeContext.Provider value={{ state, dispatch }}>
      {children}
    </ThemeContext.Provider>
  );
};
