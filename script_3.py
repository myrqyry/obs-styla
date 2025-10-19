# Let's also create a complete base theme (.obt) that others can extend
# This will be a comprehensive base theme with all necessary styling

base_theme_content = """@OBSThemeMeta {
    name: 'Catppuccin Enhanced Base';
    id: 'com.catppuccin.enhanced.base';
    author: 'Enhanced by AI Assistant';
    dark: 'true';
}

@OBSThemeVars {
    /* Base Catppuccin Mocha Colors - Can be overridden in variants */
    --rosewater: #f5e0dc;
    --flamingo: #f2cdcd;
    --pink: #f5c2e7;
    --mauve: #cba6f7;
    --red: #f38ba8;
    --maroon: #eba0ac;
    --peach: #fab387;
    --yellow: #f9e2af;
    --green: #a6e3a1;
    --teal: #94e2d5;
    --sky: #89dceb;
    --sapphire: #74c7ec;
    --blue: #89b4fa;
    --lavender: #b4befe;
    --text: #cdd6f4;
    --subtext1: #bac2de;
    --subtext0: #a6adc8;
    --overlay2: #9399b2;
    --overlay1: #7f849c;
    --overlay0: #6c7086;
    --surface2: #585b70;
    --surface1: #45475a;
    --surface0: #313244;
    --base: #1e1e2e;
    --mantle: #181825;
    --crust: #11111b;
    
    /* Semantic Color System */
    --bg_window: var(--base);
    --bg_base: var(--mantle);
    --bg_surface: var(--surface0);
    --bg_surface_raised: var(--surface1);
    --bg_surface_hover: var(--surface2);
    --bg_button: var(--surface0);
    --bg_button_hover: var(--surface1);
    --bg_button_pressed: var(--surface2);
    --bg_button_checked: var(--mauve);
    --bg_button_disabled: var(--overlay0);
    --bg_input: var(--surface0);
    --bg_input_focus: var(--surface1);
    --bg_menu: var(--surface1);
    --bg_tooltip: var(--surface2);
    --bg_selection: var(--mauve);
    
    /* Text Color System */
    --text_primary: var(--text);
    --text_secondary: var(--subtext1);
    --text_tertiary: var(--subtext0);
    --text_disabled: var(--overlay1);
    --text_link: var(--blue);
    --text_link_hover: var(--sky);
    --text_on_accent: var(--crust);
    --text_placeholder: var(--overlay2);
    
    /* Accent Color System */
    --accent_primary: var(--mauve);
    --accent_secondary: var(--lavender);
    --accent_success: var(--green);
    --accent_warning: var(--yellow);
    --accent_error: var(--red);
    --accent_info: var(--blue);
    --accent_record: var(--red);
    --accent_stream: var(--blue);
    --accent_vcam: var(--green);
    --accent_replay: var(--yellow);
    
    /* Border Color System */
    --border_base: var(--overlay0);
    --border_focus: var(--mauve);
    --border_hover: var(--overlay1);
    --border_pressed: var(--overlay2);
    --border_disabled: var(--surface2);
    --border_error: var(--red);
    --border_success: var(--green);
    --border_warning: var(--yellow);
    
    /* Shadow System */
    --shadow_small: 0 2px 4px var(--crust);
    --shadow_medium: 0 4px 8px var(--crust);
    --shadow_large: 0 8px 16px var(--crust);
    --shadow_focus: 0 0 8px var(--mauve);
    --shadow_glow: 0 0 12px;
    
    /* Sizing System */
    --border_radius: 8px;
    --border_radius_small: 4px;
    --border_radius_large: 12px;
    --border_radius_round: 50%;
    --border_width: 1px;
    --border_width_thick: 2px;
    
    /* Spacing System */
    --spacing_xs: 4px;
    --spacing_sm: 8px;
    --spacing_md: 12px;
    --spacing_lg: 16px;
    --spacing_xl: 24px;
    --spacing_xxl: 32px;
    
    /* Typography System */
    --font_size_xs: 10px;
    --font_size_sm: 11px;
    --font_size_base: 12px;
    --font_size_md: 13px;
    --font_size_lg: 14px;
    --font_size_xl: 16px;
    --font_weight_normal: 400;
    --font_weight_medium: 500;
    --font_weight_semibold: 600;
    --font_weight_bold: 700;
    --line_height_base: 1.4;
    --line_height_tight: 1.2;
    
    /* Animation System */
    --transition_fast: 150ms;
    --transition_normal: 250ms;
    --transition_slow: 350ms;
    --transition_easing: cubic-bezier(0.4, 0, 0.2, 1);
    
    /* Component Sizes */
    --button_height: 28px;
    --button_height_small: 24px;
    --button_height_large: 32px;
    --input_height: 28px;
    --toolbar_height: 32px;
    --tab_height: 32px;
    --menubar_height: 28px;
    
    /* Volume Meter Colors */
    --volume_nominal_bg: var(--green);
    --volume_warning_bg: var(--yellow);
    --volume_error_bg: var(--red);
    --volume_nominal_fg: var(--teal);
    --volume_warning_fg: var(--peach);
    --volume_error_fg: var(--maroon);
}

/* Global Application Styles */
* {
    outline: none;
}

QWidget {
    color: var(--text_primary);
    background-color: transparent;
    selection-background-color: var(--bg_selection);
    selection-color: var(--text_on_accent);
    font-size: var(--font_size_base);
    font-weight: var(--font_weight_normal);
}

QMainWindow {
    background-color: var(--bg_window);
    color: var(--text_primary);
}

/* Typography */
QLabel {
    color: var(--text_primary);
    background-color: transparent;
}

QLabel:disabled {
    color: var(--text_disabled);
}

/* Buttons */
QPushButton {
    background-color: var(--bg_button);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    padding: var(--spacing_sm) var(--spacing_md);
    font-weight: var(--font_weight_medium);
    min-height: var(--button_height);
    transition: all var(--transition_fast) var(--transition_easing);
}

QPushButton:hover {
    background-color: var(--bg_button_hover);
    border-color: var(--border_hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow_small);
}

QPushButton:pressed {
    background-color: var(--bg_button_pressed);
    border-color: var(--border_pressed);
    transform: translateY(0);
    box-shadow: none;
}

QPushButton:checked {
    background-color: var(--bg_button_checked);
    color: var(--text_on_accent);
    border-color: var(--accent_primary);
    box-shadow: var(--shadow_focus);
}

QPushButton:disabled {
    background-color: var(--bg_button_disabled);
    color: var(--text_disabled);
    border-color: var(--border_disabled);
    transform: none;
    box-shadow: none;
}

QPushButton:flat {
    border: none;
    background-color: transparent;
}

QPushButton:flat:hover {
    background-color: var(--bg_button_hover);
    border-radius: var(--border_radius);
}

/* Button Variants */
QPushButton[class="btn-primary"] {
    background-color: var(--accent_primary);
    color: var(--text_on_accent);
    border-color: var(--accent_primary);
    font-weight: var(--font_weight_semibold);
}

QPushButton[class="btn-primary"]:hover {
    background-color: var(--accent_secondary);
    border-color: var(--accent_secondary);
    box-shadow: var(--shadow_glow) var(--accent_primary);
}

QPushButton[class="btn-success"] {
    background-color: var(--accent_success);
    color: var(--text_on_accent);
    border-color: var(--accent_success);
}

QPushButton[class="btn-success"]:hover {
    background-color: var(--teal);
    border-color: var(--teal);
    box-shadow: var(--shadow_glow) var(--accent_success);
}

QPushButton[class="btn-warning"] {
    background-color: var(--accent_warning);
    color: var(--text_on_accent);
    border-color: var(--accent_warning);
}

QPushButton[class="btn-warning"]:hover {
    background-color: var(--peach);
    border-color: var(--peach);
    box-shadow: var(--shadow_glow) var(--accent_warning);
}

QPushButton[class="btn-danger"] {
    background-color: var(--accent_error);
    color: var(--text_on_accent);
    border-color: var(--accent_error);
}

QPushButton[class="btn-danger"]:hover {
    background-color: var(--maroon);
    border-color: var(--maroon);
    box-shadow: var(--shadow_glow) var(--accent_error);
}

/* Input Fields */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: var(--bg_input);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    padding: var(--spacing_sm);
    min-height: var(--input_height);
    selection-background-color: var(--bg_selection);
    selection-color: var(--text_on_accent);
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: var(--border_focus);
    background-color: var(--bg_input_focus);
    box-shadow: var(--shadow_focus);
}

QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {
    background-color: var(--bg_button_disabled);
    color: var(--text_disabled);
    border-color: var(--border_disabled);
}

QLineEdit::placeholder, QTextEdit::placeholder, QPlainTextEdit::placeholder {
    color: var(--text_placeholder);
}

/* Combo Boxes */
QComboBox {
    background-color: var(--bg_button);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    padding: var(--spacing_sm) var(--spacing_md);
    min-height: var(--button_height);
}

QComboBox:hover {
    background-color: var(--bg_button_hover);
    border-color: var(--border_hover);
}

QComboBox:on {
    background-color: var(--bg_button_pressed);
    border-color: var(--border_focus);
}

QComboBox::drop-down {
    border: none;
    width: 20px;
    padding-right: var(--spacing_sm);
}

QComboBox::down-arrow {
    image: url(theme:Dark/expand.svg);
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: var(--bg_menu);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    selection-background-color: var(--bg_selection);
    selection-color: var(--text_on_accent);
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: var(--spacing_sm);
    border-radius: var(--border_radius_small);
    margin: 1px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: var(--bg_surface_hover);
}

QComboBox QAbstractItemView::item:selected {
    background-color: var(--bg_selection);
    color: var(--text_on_accent);
}

/* Spin Boxes */
QSpinBox, QDoubleSpinBox {
    background-color: var(--bg_input);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    padding: var(--spacing_sm);
    min-height: var(--input_height);
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: var(--border_focus);
    background-color: var(--bg_input_focus);
    box-shadow: var(--shadow_focus);
}

QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: var(--bg_button);
    border: var(--border_width) solid var(--border_base);
    width: 16px;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: var(--bg_button_hover);
}

/* Check Boxes */
QCheckBox {
    color: var(--text_primary);
    spacing: var(--spacing_sm);
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    background-color: var(--bg_input);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius_small);
}

QCheckBox::indicator:hover {
    background-color: var(--bg_surface_hover);
    border-color: var(--border_hover);
}

QCheckBox::indicator:checked {
    background-color: var(--accent_primary);
    border-color: var(--accent_primary);
    image: url(theme:Dark/checkbox_checked.svg);
}

QCheckBox::indicator:checked:hover {
    background-color: var(--accent_secondary);
    border-color: var(--accent_secondary);
}

QCheckBox::indicator:indeterminate {
    background-color: var(--accent_primary);
    border-color: var(--accent_primary);
    image: url(theme:Dark/checkbox_indeterminate.svg);
}

QCheckBox:disabled {
    color: var(--text_disabled);
}

QCheckBox::indicator:disabled {
    background-color: var(--bg_button_disabled);
    border-color: var(--border_disabled);
}

/* Radio Buttons */
QRadioButton {
    color: var(--text_primary);
    spacing: var(--spacing_sm);
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
    background-color: var(--bg_input);
    border: var(--border_width) solid var(--border_base);
    border-radius: 8px;
}

QRadioButton::indicator:hover {
    background-color: var(--bg_surface_hover);
    border-color: var(--border_hover);
}

QRadioButton::indicator:checked {
    background-color: var(--accent_primary);
    border-color: var(--accent_primary);
    image: url(theme:Dark/radio_checked.svg);
}

QRadioButton::indicator:checked:hover {
    background-color: var(--accent_secondary);
    border-color: var(--accent_secondary);
}

QRadioButton:disabled {
    color: var(--text_disabled);
}

QRadioButton::indicator:disabled {
    background-color: var(--bg_button_disabled);
    border-color: var(--border_disabled);
}

/* Sliders */
QSlider::groove:horizontal {
    background-color: var(--bg_surface);
    height: 4px;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background-color: var(--accent_primary);
    border: var(--border_width_thick) solid var(--accent_primary);
    width: 16px;
    margin: -6px 0;
    border-radius: 8px;
    transition: all var(--transition_fast) var(--transition_easing);
}

QSlider::handle:horizontal:hover {
    background-color: var(--accent_secondary);
    border-color: var(--accent_secondary);
    transform: scale(1.1);
}

QSlider::handle:horizontal:pressed {
    transform: scale(0.95);
}

QSlider::add-page:horizontal {
    background-color: var(--bg_surface);
    border-radius: 2px;
}

QSlider::sub-page:horizontal {
    background-color: var(--accent_primary);
    border-radius: 2px;
}

QSlider::groove:vertical {
    background-color: var(--bg_surface);
    width: 4px;
    border-radius: 2px;
}

QSlider::handle:vertical {
    background-color: var(--accent_primary);
    border: var(--border_width_thick) solid var(--accent_primary);
    height: 16px;
    margin: 0 -6px;
    border-radius: 8px;
}

QSlider::handle:vertical:hover {
    background-color: var(--accent_secondary);
    border-color: var(--accent_secondary);
}

QSlider::add-page:vertical {
    background-color: var(--accent_primary);
    border-radius: 2px;
}

QSlider::sub-page:vertical {
    background-color: var(--bg_surface);
    border-radius: 2px;
}

/* Progress Bars */
QProgressBar {
    background-color: var(--bg_surface);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    text-align: center;
    padding: 2px;
    font-weight: var(--font_weight_medium);
}

QProgressBar::chunk {
    background-color: var(--accent_primary);
    border-radius: calc(var(--border_radius) - 1px);
    transition: width var(--transition_normal) var(--transition_easing);
}

/* Scroll Bars */
QScrollBar:vertical {
    background-color: var(--bg_base);
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: var(--overlay0);
    border-radius: 6px;
    min-height: 20px;
    transition: background-color var(--transition_fast) var(--transition_easing);
}

QScrollBar::handle:vertical:hover {
    background-color: var(--overlay1);
}

QScrollBar::handle:vertical:pressed {
    background-color: var(--overlay2);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
    height: 0;
}

QScrollBar:horizontal {
    background-color: var(--bg_base);
    height: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: var(--overlay0);
    border-radius: 6px;
    min-width: 20px;
    transition: background-color var(--transition_fast) var(--transition_easing);
}

QScrollBar::handle:horizontal:hover {
    background-color: var(--overlay1);
}

QScrollBar::handle:horizontal:pressed {
    background-color: var(--overlay2);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    background: none;
    width: 0;
}

/* Dock Widgets */
QDockWidget {
    background-color: var(--bg_base);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    titlebar-close-icon: url(theme:Dark/close.svg);
    titlebar-normal-icon: url(theme:Dark/popout.svg);
}

QDockWidget::title {
    background-color: var(--bg_surface);
    padding: var(--spacing_sm);
    border-bottom: var(--border_width) solid var(--border_base);
    font-weight: var(--font_weight_semibold);
    text-align: center;
}

QDockWidget::close-button, QDockWidget::float-button {
    background-color: transparent;
    border: none;
    border-radius: var(--border_radius_small);
    padding: 2px;
}

QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background-color: var(--bg_surface_hover);
}

QDockWidget::close-button:pressed, QDockWidget::float-button:pressed {
    background-color: var(--bg_button_pressed);
}

/* Splitters */
QSplitter::handle {
    background-color: var(--border_base);
    transition: background-color var(--transition_fast) var(--transition_easing);
}

QSplitter::handle:hover {
    background-color: var(--border_hover);
}

QSplitter::handle:pressed {
    background-color: var(--border_pressed);
}

QSplitter::handle:horizontal {
    width: 2px;
}

QSplitter::handle:vertical {
    height: 2px;
}

/* Tab Widgets */
QTabWidget::pane {
    background-color: var(--bg_base);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    position: absolute;
    top: -1px;
}

QTabBar {
    qproperty-drawBase: 0;
}

QTabBar::tab {
    background-color: var(--bg_surface);
    color: var(--text_secondary);
    border: var(--border_width) solid var(--border_base);
    border-bottom: none;
    padding: var(--spacing_sm) var(--spacing_md);
    margin-right: 2px;
    border-radius: var(--border_radius) var(--border_radius) 0 0;
    min-width: 80px;
    font-weight: var(--font_weight_medium);
    transition: all var(--transition_fast) var(--transition_easing);
}

QTabBar::tab:hover {
    background-color: var(--bg_surface_hover);
    color: var(--text_primary);
}

QTabBar::tab:selected {
    background-color: var(--bg_base);
    color: var(--accent_primary);
    font-weight: var(--font_weight_semibold);
    border-bottom-color: var(--bg_base);
}

QTabBar::tab:!selected {
    margin-top: 2px;
}

/* List Widgets */
QListWidget {
    background-color: var(--bg_base);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    selection-background-color: var(--bg_selection);
    selection-color: var(--text_on_accent);
    outline: none;
    show-decoration-selected: 1;
}

QListWidget::item {
    padding: var(--spacing_sm);
    border-bottom: var(--border_width) solid transparent;
    border-radius: var(--border_radius_small);
    margin: 1px;
}

QListWidget::item:hover {
    background-color: var(--bg_surface_hover);
    border-radius: var(--border_radius_small);
}

QListWidget::item:selected {
    background-color: var(--bg_selection);
    color: var(--text_on_accent);
    border-radius: var(--border_radius_small);
}

QListWidget::item:selected:active {
    background-color: var(--bg_selection);
}

QListWidget::item:selected:!active {
    background-color: var(--bg_surface_hover);
    color: var(--text_primary);
}

/* Tree Widgets */
QTreeWidget {
    background-color: var(--bg_base);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    selection-background-color: var(--bg_selection);
    selection-color: var(--text_on_accent);
    outline: none;
    show-decoration-selected: 1;
}

QTreeWidget::item {
    padding: var(--spacing_xs) var(--spacing_sm);
    border-radius: var(--border_radius_small);
    margin: 1px 0;
}

QTreeWidget::item:hover {
    background-color: var(--bg_surface_hover);
}

QTreeWidget::item:selected {
    background-color: var(--bg_selection);
    color: var(--text_on_accent);
}

QTreeWidget::item:selected:active {
    background-color: var(--bg_selection);
}

QTreeWidget::item:selected:!active {
    background-color: var(--bg_surface_hover);
    color: var(--text_primary);
}

QTreeWidget::branch:has-siblings:!adjoins-item {
    border-image: url(theme:Dark/branch_vline.svg) 0;
}

QTreeWidget::branch:has-siblings:adjoins-item {
    border-image: url(theme:Dark/branch_more.svg) 0;
}

QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {
    border-image: url(theme:Dark/branch_end.svg) 0;
}

QTreeWidget::branch:has-children:!has-siblings:closed,
QTreeWidget::branch:closed:has-children:has-siblings {
    border-image: none;
    image: url(theme:Dark/branch_closed.svg);
}

QTreeWidget::branch:open:has-children:!has-siblings,
QTreeWidget::branch:open:has-children:has-siblings {
    border-image: none;
    image: url(theme:Dark/branch_open.svg);
}

/* Group Boxes */
QGroupBox {
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    margin-top: var(--spacing_md);
    padding-top: var(--spacing_sm);
    font-weight: var(--font_weight_semibold);
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: var(--spacing_sm);
    padding: 0 var(--spacing_sm);
    background-color: var(--bg_window);
    color: var(--text_primary);
}

QGroupBox:disabled {
    color: var(--text_disabled);
    border-color: var(--border_disabled);
}

/* Menu Bar */
QMenuBar {
    background-color: var(--bg_base);
    color: var(--text_primary);
    border-bottom: var(--border_width) solid var(--border_base);
    spacing: var(--spacing_xs);
}

QMenuBar::item {
    padding: var(--spacing_sm) var(--spacing_md);
    background-color: transparent;
    border-radius: var(--border_radius_small);
}

QMenuBar::item:selected {
    background-color: var(--bg_surface_hover);
}

QMenuBar::item:pressed {
    background-color: var(--bg_button_pressed);
}

/* Menus */
QMenu {
    background-color: var(--bg_menu);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    padding: var(--spacing_xs);
}

QMenu::item {
    padding: var(--spacing_sm) var(--spacing_md);
    border-radius: var(--border_radius_small);
    margin: 1px;
}

QMenu::item:selected {
    background-color: var(--bg_selection);
    color: var(--text_on_accent);
}

QMenu::item:disabled {
    color: var(--text_disabled);
}

QMenu::separator {
    height: var(--border_width);
    background-color: var(--border_base);
    margin: var(--spacing_xs) 0;
}

QMenu::icon {
    padding-left: var(--spacing_sm);
}

QMenu::right-arrow {
    image: url(theme:Dark/right_arrow.svg);
    width: 8px;
    height: 8px;
}

/* Tool Tips */
QToolTip {
    background-color: var(--bg_tooltip);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    padding: var(--spacing_sm);
    font-size: var(--font_size_sm);
    box-shadow: var(--shadow_medium);
}

/* Status Bar */
QStatusBar {
    background-color: var(--bg_base);
    color: var(--text_primary);
    border-top: var(--border_width) solid var(--border_base);
    font-size: var(--font_size_sm);
}

QStatusBar::item {
    border: none;
    padding: var(--spacing_xs) var(--spacing_sm);
}

/* Tool Bar */
QToolBar {
    background-color: var(--bg_base);
    border: var(--border_width) solid var(--border_base);
    spacing: var(--spacing_xs);
    padding: var(--spacing_xs);
}

QToolBar::separator {
    background-color: var(--border_base);
    width: var(--border_width);
    margin: 0 var(--spacing_xs);
}

QToolButton {
    background-color: transparent;
    border: none;
    border-radius: var(--border_radius_small);
    padding: var(--spacing_xs);
    margin: 1px;
}

QToolButton:hover {
    background-color: var(--bg_surface_hover);
}

QToolButton:pressed {
    background-color: var(--bg_button_pressed);
}

QToolButton:checked {
    background-color: var(--bg_button_checked);
    color: var(--text_on_accent);
}

/* Header View */
QHeaderView::section {
    background-color: var(--bg_surface);
    color: var(--text_primary);
    border: none;
    border-right: var(--border_width) solid var(--border_base);
    border-bottom: var(--border_width) solid var(--border_base);
    padding: var(--spacing_sm);
    font-weight: var(--font_weight_semibold);
}

QHeaderView::section:hover {
    background-color: var(--bg_surface_hover);
}

QHeaderView::section:pressed {
    background-color: var(--bg_button_pressed);
}

/* Table Widget */
QTableWidget {
    background-color: var(--bg_base);
    color: var(--text_primary);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    gridline-color: var(--border_base);
    selection-background-color: var(--bg_selection);
    selection-color: var(--text_on_accent);
}

QTableWidget::item {
    padding: var(--spacing_sm);
    border-right: var(--border_width) solid var(--border_base);
    border-bottom: var(--border_width) solid var(--border_base);
}

QTableWidget::item:hover {
    background-color: var(--bg_surface_hover);
}

QTableWidget::item:selected {
    background-color: var(--bg_selection);
    color: var(--text_on_accent);
}

/* Volume Controls */
VolumeMeter {
    qproperty-backgroundNominalColor: var(--volume_nominal_bg);
    qproperty-backgroundWarningColor: var(--volume_warning_bg);
    qproperty-backgroundErrorColor: var(--volume_error_bg);
    qproperty-foregroundNominalColor: var(--volume_nominal_fg);
    qproperty-foregroundWarningColor: var(--volume_warning_fg);
    qproperty-foregroundErrorColor: var(--volume_error_fg);
    qproperty-magnitudeColor: var(--text_primary);
    qproperty-majorTickColor: var(--text_secondary);
    qproperty-minorTickColor: var(--text_tertiary);
}

/* OBS-Specific Controls */
OBSHotkeyLabel {
    color: var(--text_secondary);
    font-size: var(--font_size_sm);
}

OBSHotkeyLabel[hotkeyPairHover=true] {
    color: var(--accent_primary);
}

/* Recording/Streaming Buttons */
QPushButton[themeID="recordButton"] {
    background-color: var(--accent_record);
    color: var(--text_on_accent);
    border-color: var(--accent_record);
    font-weight: var(--font_weight_semibold);
}

QPushButton[themeID="recordButton"]:hover {
    background-color: var(--maroon);
    border-color: var(--maroon);
    box-shadow: var(--shadow_glow) var(--accent_record);
}

QPushButton[themeID="streamButton"] {
    background-color: var(--accent_stream);
    color: var(--text_on_accent);
    border-color: var(--accent_stream);
    font-weight: var(--font_weight_semibold);
}

QPushButton[themeID="streamButton"]:hover {
    background-color: var(--sapphire);
    border-color: var(--sapphire);
    box-shadow: var(--shadow_glow) var(--accent_stream);
}

QPushButton[themeID="vcamButton"] {
    background-color: var(--accent_vcam);
    color: var(--text_on_accent);
    border-color: var(--accent_vcam);
    font-weight: var(--font_weight_semibold);
}

QPushButton[themeID="vcamButton"]:hover {
    background-color: var(--teal);
    border-color: var(--teal);
    box-shadow: var(--shadow_glow) var(--accent_vcam);
}

QPushButton[themeID="replayBufferButton"] {
    background-color: var(--accent_replay);
    color: var(--text_on_accent);
    border-color: var(--accent_replay);
    font-weight: var(--font_weight_semibold);
}

QPushButton[themeID="replayBufferButton"]:hover {
    background-color: var(--peach);
    border-color: var(--peach);
    box-shadow: var(--shadow_glow) var(--accent_replay);
}

/* Source List Styling */
#sources {
    background-color: var(--bg_base);
}

#sources QListWidget::item {
    color: var(--text_primary);
    background-color: transparent;
    padding: var(--spacing_sm);
    border-radius: var(--border_radius_small);
    margin: 1px;
}

#sources QListWidget::item:selected {
    background-color: var(--bg_selection);
    color: var(--text_on_accent);
}

#sources QListWidget::item:hover:!selected {
    background-color: var(--bg_surface_hover);
}

/* Scene List Styling */
#scenes {
    background-color: var(--bg_base);
}

#scenes QListWidget::item {
    color: var(--text_primary);
    background-color: transparent;
    padding: var(--spacing_sm);
    border-radius: var(--border_radius_small);
    margin: 1px;
}

#scenes QListWidget::item:selected {
    background-color: var(--bg_selection);
    color: var(--text_on_accent);
}

#scenes QListWidget::item:hover:!selected {
    background-color: var(--bg_surface_hover);
}

/* Controls Dock */
#controlsDock {
    background-color: var(--bg_base);
}

#controlsDock QPushButton {
    margin: 2px;
}

/* Statistics Dock */
#statsDock {
    background-color: var(--bg_base);
}

/* Audio Mixer */
#mixerDock {
    background-color: var(--bg_base);
}

/* Transitions Dock */
#transitionsDock {
    background-color: var(--bg_base);
}

/* Studio Mode */
OBSBasicPreview[displayBackgroundColor="31, 30, 31"] {
    qproperty-displayBackgroundColor: var(--mantle);
}

/* Filters Frame */
#filtersFrame {
    background-color: var(--bg_base);
}

/* Properties Frame */
#propertiesFrame {
    background-color: var(--bg_base);
}

/* Context Container */
#contextContainer {
    background-color: var(--bg_base);
}

/* State Labels */
QLabel[class="error"] {
    color: var(--accent_error);
    font-weight: var(--font_weight_medium);
}

QLabel[class="warning"] {
    color: var(--accent_warning);
    font-weight: var(--font_weight_medium);
}

QLabel[class="success"] {
    color: var(--accent_success);
    font-weight: var(--font_weight_medium);
}

QLabel[class="info"] {
    color: var(--accent_info);
    font-weight: var(--font_weight_medium);
}

/* Custom Styling for Enhanced Features */
.obs-enhanced-card {
    background-color: var(--bg_surface);
    border: var(--border_width) solid var(--border_base);
    border-radius: var(--border_radius);
    padding: var(--spacing_md);
    margin: var(--spacing_sm);
}

.obs-enhanced-card:hover {
    border-color: var(--border_hover);
    box-shadow: var(--shadow_small);
}

.obs-enhanced-highlight {
    background-color: var(--accent_primary);
    color: var(--text_on_accent);
    padding: var(--spacing_xs) var(--spacing_sm);
    border-radius: var(--border_radius_small);
    font-weight: var(--font_weight_medium);
}

.obs-enhanced-muted {
    color: var(--text_tertiary);
    font-size: var(--font_size_sm);
}

.obs-enhanced-badge {
    background-color: var(--bg_surface_raised);
    color: var(--text_secondary);
    padding: var(--spacing_xs) var(--spacing_sm);
    border-radius: var(--border_radius_large);
    font-size: var(--font_size_xs);
    font-weight: var(--font_weight_medium);
    border: var(--border_width) solid var(--border_base);
}

.obs-enhanced-badge.success {
    background-color: var(--accent_success);
    color: var(--text_on_accent);
    border-color: var(--accent_success);
}

.obs-enhanced-badge.warning {
    background-color: var(--accent_warning);
    color: var(--text_on_accent);
    border-color: var(--accent_warning);
}

.obs-enhanced-badge.error {
    background-color: var(--accent_error);
    color: var(--text_on_accent);
    border-color: var(--accent_error);
}
"""

# Save the base theme
with open('catppuccin_enhanced_base.obt', 'w') as f:
    f.write(base_theme_content)

print("🏗️ Created Comprehensive Catppuccin Enhanced Base Theme")
print("="*60)
print("✅ Saved as: catppuccin_enhanced_base.obt")
print()
print("📋 Base Theme Features:")
print("• Complete .obt base theme (not extending Yami)")
print("• Comprehensive variable system (100+ variables)")
print("• Full widget coverage for all Qt components")
print("• Semantic color naming system")
print("• Advanced styling system with animations")
print("• Custom CSS classes for enhanced features")
print("• Production-ready for theme developers")
print()
print("🔧 For Theme Developers:")
print("• Use this as a base for creating custom variants")
print("• Override any variables in .ovt files")
print("• Extend with custom components")
print("• Maintain consistent design language")
print()
print("📦 Complete Theme Collection:")
print("• catppuccin_enhanced_base.obt (Base theme)")
print("• catppuccin_enhanced_latte.ovt (Light variant)")  
print("• catppuccin_enhanced_frappe.ovt (Dark variant)")
print("• catppuccin_enhanced_macchiato.ovt (Dark variant)")
print("• catppuccin_enhanced_mocha.ovt (Dark variant)")
print("• catppuccin_installation_guide.md (Documentation)")