"""
Settings Window for WDock
Comprehensive configuration interface for all WDock settings
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QWidget, QLabel, QPushButton, QCheckBox, QComboBox,
                             QSpinBox, QSlider, QGroupBox, QRadioButton, 
                             QButtonGroup, QFileDialog, QLineEdit, QTextEdit,
                             QFormLayout, QGridLayout, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor

from ..utils.startup_manager import StartupManager
from ..utils.lucide_icons import get_wdock_icon


class SettingsWindow(QDialog):
    """Settings dialog for WDock configuration"""
    
    # Signals
    settings_changed = pyqtSignal()
    position_changed = pyqtSignal(str)
    alignment_changed = pyqtSignal(str)
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.startup_manager = StartupManager()
        self.setWindowTitle("Настройки WDock")
        self.setFixedSize(500, 600)
        self.setModal(True)
        
        # Remove question mark button
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )
        
        self.setup_ui()
        self.load_settings()
        self.apply_styles()
        
        # Connect theme change signal
        if hasattr(self, 'theme_group'):
            self.theme_group.buttonClicked.connect(self.on_theme_changed)
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Add tabs
        self.create_general_tab()
        self.create_appearance_tab()
        self.create_behavior_tab()
        self.create_advanced_tab()
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Reset to defaults
        reset_button = QPushButton("Сбросить")
        reset_button.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(reset_button)
        
        button_layout.addStretch()
        
        # Cancel and OK buttons
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept_settings)
        ok_button.setDefault(True)
        button_layout.addWidget(ok_button)
        
        # Apply button
        apply_button = QPushButton("Применить")
        apply_button.clicked.connect(self.apply_settings)
        button_layout.addWidget(apply_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_general_tab(self):
        """Create general settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Position group
        position_group = QGroupBox("Расположение дока")
        position_layout = QGridLayout()
        
        self.position_group = QButtonGroup()
        positions = [
            ("Верх", "top", 0, 1),
            ("Лево", "left", 1, 0),
            ("Право", "right", 1, 2),
            ("Низ", "bottom", 2, 1)
        ]
        
        for text, value, row, col in positions:
            radio = QRadioButton(text)
            radio.setProperty("position", value)
            self.position_group.addButton(radio)
            position_layout.addWidget(radio, row, col)
        
        position_group.setLayout(position_layout)
        layout.addWidget(position_group)
        
        # Alignment group
        alignment_group = QGroupBox("Выравнивание")
        alignment_layout = QHBoxLayout()
        
        self.alignment_group = QButtonGroup()
        alignments = [
            ("Начало", "start"),
            ("Центр", "center"),
            ("Конец", "end")
        ]
        
        for text, value in alignments:
            radio = QRadioButton(text)
            radio.setProperty("alignment", value)
            self.alignment_group.addButton(radio)
            alignment_layout.addWidget(radio)
        
        alignment_group.setLayout(alignment_layout)
        layout.addWidget(alignment_group)
        
        # Auto-startup
        self.startup_checkbox = QCheckBox("Запускать при старте Windows")
        self.startup_checkbox.toggled.connect(self.on_startup_toggled)
        layout.addWidget(self.startup_checkbox)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Общие")
        
        # Add icon to tab if available
        general_icon = get_wdock_icon("settings_main", size=16, is_dark=self.get_current_theme_is_dark())
        if general_icon:
            self.tab_widget.setTabIcon(0, general_icon)
    
    def create_appearance_tab(self):
        """Create appearance settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Theme group
        theme_group = QGroupBox("Тема оформления")
        theme_layout = QVBoxLayout()
        
        self.theme_group = QButtonGroup()
        themes = [
            ("Автоматически (следовать системе)", "auto"),
            ("Светлая тема", "light"),
            ("Темная тема", "dark")
        ]
        
        for text, value in themes:
            radio = QRadioButton(text)
            radio.setProperty("theme", value)
            self.theme_group.addButton(radio)
            theme_layout.addWidget(radio)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Icon size
        icon_size_group = QGroupBox("Размер иконок")
        icon_size_layout = QFormLayout()
        
        self.icon_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.icon_size_slider.setRange(32, 64)
        self.icon_size_slider.setValue(48)
        self.icon_size_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.icon_size_slider.setTickInterval(8)
        
        self.icon_size_label = QLabel("48 px")
        self.icon_size_slider.valueChanged.connect(
            lambda v: self.icon_size_label.setText(f"{v} px")
        )
        
        icon_size_layout.addRow("Размер:", self.icon_size_slider)
        icon_size_layout.addRow("", self.icon_size_label)
        icon_size_group.setLayout(icon_size_layout)
        layout.addWidget(icon_size_group)
        
        # Animation settings
        animation_group = QGroupBox("Анимации")
        animation_layout = QFormLayout()
        
        self.animation_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.animation_speed_slider.setRange(100, 500)
        self.animation_speed_slider.setValue(200)
        self.animation_speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.animation_speed_slider.setTickInterval(100)
        
        self.animation_speed_label = QLabel("200 мс")
        self.animation_speed_slider.valueChanged.connect(
            lambda v: self.animation_speed_label.setText(f"{v} мс")
        )
        
        animation_layout.addRow("Скорость:", self.animation_speed_slider)
        animation_layout.addRow("", self.animation_speed_label)
        animation_group.setLayout(animation_layout)
        layout.addWidget(animation_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Внешний вид")
        
        # Add icon to tab if available
        appearance_icon = get_wdock_icon("theme_auto", size=16, is_dark=self.get_current_theme_is_dark())
        if appearance_icon:
            self.tab_widget.setTabIcon(1, appearance_icon)
    
    def create_behavior_tab(self):
        """Create behavior settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Auto-hide group
        hide_group = QGroupBox("Автоскрытие")
        hide_layout = QVBoxLayout()
        
        self.auto_hide_checkbox = QCheckBox("Включить автоскрытие")
        hide_layout.addWidget(self.auto_hide_checkbox)
        
        self.intelligent_hide_checkbox = QCheckBox("Умное скрытие (при полноэкранных приложениях)")
        hide_layout.addWidget(self.intelligent_hide_checkbox)
        
        # Auto-hide delay
        delay_layout = QFormLayout()
        self.auto_hide_delay = QSpinBox()
        self.auto_hide_delay.setRange(100, 5000)
        self.auto_hide_delay.setValue(500)
        self.auto_hide_delay.setSuffix(" мс")
        delay_layout.addRow("Задержка скрытия:", self.auto_hide_delay)
        
        hide_layout.addLayout(delay_layout)
        hide_group.setLayout(hide_layout)
        layout.addWidget(hide_group)
        
        # System tray
        tray_group = QGroupBox("Системный трей")
        tray_layout = QVBoxLayout()
        
        self.show_tray_checkbox = QCheckBox("Показывать иконку в системном трее")
        tray_layout.addWidget(self.show_tray_checkbox)
        
        self.minimize_to_tray_checkbox = QCheckBox("Сворачивать в трей при закрытии")
        tray_layout.addWidget(self.minimize_to_tray_checkbox)
        
        tray_group.setLayout(tray_layout)
        layout.addWidget(tray_group)
        
        # Hotkeys group
        hotkeys_group = QGroupBox("Горячие клавиши")
        hotkeys_layout = QFormLayout()
        
        self.toggle_hotkey = QLineEdit()
        self.toggle_hotkey.setPlaceholderText("Win+D")
        self.toggle_hotkey.setReadOnly(True)  # For future implementation
        hotkeys_layout.addRow("Показать/скрыть док:", self.toggle_hotkey)
        
        hotkeys_group.setLayout(hotkeys_layout)
        layout.addWidget(hotkeys_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Поведение")
        
        # Add icon to tab if available
        behavior_icon = get_wdock_icon("settings_main", size=16, is_dark=self.get_current_theme_is_dark())
        if behavior_icon:
            self.tab_widget.setTabIcon(2, behavior_icon)
    
    def create_advanced_tab(self):
        """Create advanced settings tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Performance group
        performance_group = QGroupBox("Производительность")
        performance_layout = QFormLayout()
        
        self.memory_limit = QSpinBox()
        self.memory_limit.setRange(25, 200)
        self.memory_limit.setValue(50)
        self.memory_limit.setSuffix(" МБ")
        performance_layout.addRow("Лимит памяти:", self.memory_limit)
        
        self.update_interval = QSpinBox()
        self.update_interval.setRange(100, 2000)
        self.update_interval.setValue(500)
        self.update_interval.setSuffix(" мс")
        performance_layout.addRow("Интервал обновления:", self.update_interval)
        
        performance_group.setLayout(performance_layout)
        layout.addWidget(performance_group)
        
        # Debug group
        debug_group = QGroupBox("Отладка")
        debug_layout = QVBoxLayout()
        
        self.debug_mode_checkbox = QCheckBox("Режим отладки")
        debug_layout.addWidget(self.debug_mode_checkbox)
        
        self.show_borders_checkbox = QCheckBox("Показывать границы виджетов")
        debug_layout.addWidget(self.show_borders_checkbox)
        
        debug_group.setLayout(debug_layout)
        layout.addWidget(debug_group)
        
        # Config management
        config_group = QGroupBox("Управление конфигурацией")
        config_layout = QVBoxLayout()
        
        config_buttons_layout = QHBoxLayout()
        
        export_button = QPushButton("Экспорт настроек...")
        export_button.clicked.connect(self.export_config)
        config_buttons_layout.addWidget(export_button)
        
        import_button = QPushButton("Импорт настроек...")
        import_button.clicked.connect(self.import_config)
        config_buttons_layout.addWidget(import_button)
        
        config_layout.addLayout(config_buttons_layout)
        
        # Config location
        config_info = QLabel(f"Файл конфигурации: {self.config_manager.config_file}")
        config_info.setWordWrap(True)
        config_info.setStyleSheet("color: #666666; font-size: 10px;")
        config_layout.addWidget(config_info)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Дополнительно")
        
        # Add icon to tab if available
        advanced_icon = get_wdock_icon("settings_main", size=16, is_dark=self.get_current_theme_is_dark())
        if advanced_icon:
            self.tab_widget.setTabIcon(3, advanced_icon)
    
    def load_settings(self):
        """Load current settings into the UI"""
        # Position
        current_position = self.config_manager.get("position", "bottom")
        for button in self.position_group.buttons():
            if button.property("position") == current_position:
                button.setChecked(True)
                break
        
        # Alignment
        current_alignment = self.config_manager.get("alignment", "center")
        for button in self.alignment_group.buttons():
            if button.property("alignment") == current_alignment:
                button.setChecked(True)
                break
        
        # Theme
        current_theme = self.config_manager.get("theme", "auto")
        for button in self.theme_group.buttons():
            if button.property("theme") == current_theme:
                button.setChecked(True)
                break
        
        # Checkboxes
        self.auto_hide_checkbox.setChecked(self.config_manager.get("auto_hide", True))
        self.intelligent_hide_checkbox.setChecked(self.config_manager.get("intelligent_hide", True))
        self.show_tray_checkbox.setChecked(self.config_manager.get("show_tray", True))
        self.minimize_to_tray_checkbox.setChecked(self.config_manager.get("minimize_to_tray", True))
        self.debug_mode_checkbox.setChecked(self.config_manager.get("debug_mode", False))
        self.show_borders_checkbox.setChecked(self.config_manager.get("show_borders", False))
        
        # Startup status
        self.startup_checkbox.setChecked(self.startup_manager.is_startup_enabled())
        
        # Sliders and spinboxes
        self.icon_size_slider.setValue(self.config_manager.get("icon_size", 48))
        self.animation_speed_slider.setValue(self.config_manager.get("animation_speed", 200))
        self.auto_hide_delay.setValue(self.config_manager.get("auto_hide_delay", 500))
        self.memory_limit.setValue(self.config_manager.get("memory_limit", 50))
        self.update_interval.setValue(self.config_manager.get("update_interval", 500))
        
        # Update labels
        self.icon_size_label.setText(f"{self.icon_size_slider.value()} px")
        self.animation_speed_label.setText(f"{self.animation_speed_slider.value()} мс")
    
    def apply_settings(self):
        """Apply current settings without closing dialog"""
        self.save_settings()
        
        # Refresh theme after settings change
        self.apply_styles()
        
        self.settings_changed.emit()
        
        # Show confirmation
        QMessageBox.information(self, "Настройки", "Настройки применены!")
    
    def accept_settings(self):
        """Accept and save settings"""
        self.save_settings()
        
        # Refresh theme after settings change
        self.apply_styles()
        
        self.settings_changed.emit()
        self.accept()
    
    def save_settings(self):
        """Save current settings to config"""
        # Position
        for button in self.position_group.buttons():
            if button.isChecked():
                position = button.property("position")
                self.config_manager.set("position", position)
                self.position_changed.emit(position)
                break
        
        # Alignment
        for button in self.alignment_group.buttons():
            if button.isChecked():
                alignment = button.property("alignment")
                self.config_manager.set("alignment", alignment)
                self.alignment_changed.emit(alignment)
                break
        
        # Theme
        for button in self.theme_group.buttons():
            if button.isChecked():
                self.config_manager.set("theme", button.property("theme"))
                break
        
        # Checkboxes
        self.config_manager.set("auto_hide", self.auto_hide_checkbox.isChecked())
        self.config_manager.set("intelligent_hide", self.intelligent_hide_checkbox.isChecked())
        self.config_manager.set("show_tray", self.show_tray_checkbox.isChecked())
        self.config_manager.set("minimize_to_tray", self.minimize_to_tray_checkbox.isChecked())
        self.config_manager.set("debug_mode", self.debug_mode_checkbox.isChecked())
        self.config_manager.set("show_borders", self.show_borders_checkbox.isChecked())
        
        # Sliders and spinboxes
        self.config_manager.set("icon_size", self.icon_size_slider.value())
        self.config_manager.set("animation_speed", self.animation_speed_slider.value())
        self.config_manager.set("auto_hide_delay", self.auto_hide_delay.value())
        self.config_manager.set("memory_limit", self.memory_limit.value())
        self.config_manager.set("update_interval", self.update_interval.value())
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, "Сброс настроек",
            "Сбросить все настройки к значениям по умолчанию?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Reset config to defaults
            self.config_manager.config = self.config_manager.default_config.copy()
            self.config_manager.save_config()
            
            # Reload UI
            self.load_settings()
            
            QMessageBox.information(self, "Сброс настроек", "Настройки сброшены к значениям по умолчанию!")
    
    def export_config(self):
        """Export configuration to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Экспорт настроек", 
            "wdock_config.json", 
            "JSON Files (*.json)"
        )
        
        if filename:
            try:
                import shutil
                shutil.copy2(self.config_manager.config_file, filename)
                QMessageBox.information(self, "Экспорт", f"Настройки экспортированы в:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка экспорта", f"Не удалось экспортировать настройки:\n{e}")
    
    def import_config(self):
        """Import configuration from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Импорт настроек", 
            "", 
            "JSON Files (*.json)"
        )
        
        if filename:
            reply = QMessageBox.question(
                self, "Импорт настроек",
                "Импорт настроек заменит текущую конфигурацию.\nПродолжить?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    import shutil
                    shutil.copy2(filename, self.config_manager.config_file)
                    
                    # Reload config
                    self.config_manager.config = self.config_manager.load_config()
                    self.load_settings()
                    
                    QMessageBox.information(self, "Импорт", "Настройки успешно импортированы!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка импорта", f"Не удалось импортировать настройки:\n{e}")
    
    def on_startup_toggled(self, checked: bool):
        """Обработка изменения статуса автозапуска"""
        if checked:
            success = self.startup_manager.enable_startup()
            if not success:
                QMessageBox.warning(
                    self, "Ошибка", 
                    "Не удалось включить автозапуск.\nПроверьте права доступа."
                )
                self.startup_checkbox.setChecked(False)
        else:
            success = self.startup_manager.disable_startup()
            if not success:
                QMessageBox.warning(
                    self, "Ошибка", 
                    "Не удалось отключить автозапуск.\nПроверьте права доступа."
                )
                self.startup_checkbox.setChecked(True)
    
    def get_current_theme_is_dark(self) -> bool:
        """Get whether current theme should be dark based on configuration"""
        theme = self.config_manager.get("theme", "auto")
        if theme == "auto":
            return self.is_dark_theme()
        else:
            return theme == "dark"
    
    def on_theme_changed(self):
        """Handle theme change in settings"""
        # Reapply styles when theme changes
        self.apply_styles()
        
        # Update tab icons with new theme
        is_dark = self.get_current_theme_is_dark()
        
        # Update all tab icons
        icons = [
            ("settings_main", 0),
            ("theme_auto", 1), 
            ("settings_main", 2),
            ("settings_main", 3)
        ]
        
        for icon_name, tab_index in icons:
            icon = get_wdock_icon(icon_name, size=16, is_dark=is_dark)
            if icon:
                self.tab_widget.setTabIcon(tab_index, icon)
    
    def apply_styles(self):
        """Apply custom styles to the dialog based on system theme"""
        # Apply theme-appropriate styles
        if self.get_current_theme_is_dark():
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
    
    def is_dark_theme(self) -> bool:
        """Detect if Windows is using dark theme"""
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return value == 0  # 0 = dark theme, 1 = light theme
        except:
            return False  # Default to light theme
    
    def apply_light_theme(self):
        """Apply light theme styles"""
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F5F5;
                color: #000000;
            }
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                background-color: white;
                border-radius: 4px;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: #E0E0E0;
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                padding: 8px 16px;
                margin-right: 2px;
                color: #000000;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-color: #CCCCCC;
                color: #000000;
            }
            QTabBar::tab:hover {
                background-color: #F0F0F0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #CCCCCC;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #000000;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: white;
                color: #000000;
            }
            QLabel {
                color: #000000;
                background-color: transparent;
            }
            QPushButton {
                background-color: #F0F0F0;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 11px;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
                border-color: #AAAAAA;
            }
            QPushButton:pressed {
                background-color: #D0D0D0;
            }
            QPushButton:default {
                background-color: #007ACC;
                color: white;
                border-color: #005A9E;
            }
            QPushButton:default:hover {
                background-color: #005A9E;
            }
            QCheckBox {
                color: #000000;
                background-color: transparent;
            }
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid #CCCCCC;
                border-radius: 2px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #007ACC;
                border-color: #005A9E;
            }
            QRadioButton {
                color: #000000;
                background-color: transparent;
            }
            QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid #CCCCCC;
                border-radius: 7px;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                background-color: #007ACC;
                border-color: #005A9E;
            }
            QSpinBox, QLineEdit {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 2px;
                padding: 4px;
                color: #000000;
            }
            QSpinBox:focus, QLineEdit:focus {
                border-color: #007ACC;
            }
            QSlider::groove:horizontal {
                border: 1px solid #CCCCCC;
                height: 4px;
                background: #F0F0F0;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #007ACC;
                border: 1px solid #005A9E;
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #005A9E;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 2px;
                color: #000000;
            }
        """)
    
    def apply_dark_theme(self):
        """Apply dark theme styles"""
        self.setStyleSheet("""
            QDialog {
                background-color: #2B2B2B;
                color: #FFFFFF;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #3C3C3C;
                border-radius: 4px;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: #404040;
                border: 1px solid #555555;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                padding: 8px 16px;
                margin-right: 2px;
                color: #FFFFFF;
            }
            QTabBar::tab:selected {
                background-color: #3C3C3C;
                border-color: #555555;
                color: #FFFFFF;
            }
            QTabBar::tab:hover {
                background-color: #4A4A4A;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #FFFFFF;
                background-color: #3C3C3C;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #3C3C3C;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
                background-color: transparent;
            }
            QPushButton {
                background-color: #404040;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 11px;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #4A4A4A;
                border-color: #777777;
            }
            QPushButton:pressed {
                background-color: #353535;
            }
            QPushButton:default {
                background-color: #007ACC;
                color: white;
                border-color: #005A9E;
            }
            QPushButton:default:hover {
                background-color: #005A9E;
            }
            QCheckBox {
                color: #FFFFFF;
                background-color: transparent;
            }
            QCheckBox::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid #555555;
                border-radius: 2px;
                background-color: #3C3C3C;
            }
            QCheckBox::indicator:checked {
                background-color: #007ACC;
                border-color: #005A9E;
            }
            QRadioButton {
                color: #FFFFFF;
                background-color: transparent;
            }
            QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid #555555;
                border-radius: 7px;
                background-color: #3C3C3C;
            }
            QRadioButton::indicator:checked {
                background-color: #007ACC;
                border-color: #005A9E;
            }
            QSpinBox, QLineEdit {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 2px;
                padding: 4px;
                color: #FFFFFF;
            }
            QSpinBox:focus, QLineEdit:focus {
                border-color: #007ACC;
            }
            QSlider::groove:horizontal {
                border: 1px solid #555555;
                height: 4px;
                background: #404040;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #007ACC;
                border: 1px solid #005A9E;
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #005A9E;
            }
            QTextEdit {
                background-color: #3C3C3C;
                border: 1px solid #555555;
                border-radius: 2px;
                color: #FFFFFF;
            }
        """)