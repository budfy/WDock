"""
System Tray for WDock
Provides system tray icon and menu for background operation
"""

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor, QAction
import sys

from ..utils.lucide_icons import get_wdock_icon, get_lucide_icons


class SystemTrayManager(QObject):
    """Manages the system tray icon and menu"""
    
    # Signals
    show_dock_requested = pyqtSignal()
    hide_dock_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    about_requested = pyqtSignal()
    quit_requested = pyqtSignal()
    dock_context_menu_requested = pyqtSignal()
    
    def __init__(self, config_manager, dock_window=None, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.dock_window = dock_window
        self.tray_icon = None
        self.tray_menu = None
        
        self.create_tray_icon()
        self.create_tray_menu()
        self.setup_connections()
    
    def create_tray_icon(self):
        """Create the system tray icon"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(
                None, "WDock",
                "Системний трей недоступний в цій системі."
            )
            return False
        
        # Create custom icon
        icon_pixmap = self.create_tray_icon_pixmap()
        icon = QIcon(icon_pixmap)
        
        self.tray_icon = QSystemTrayIcon(icon)
        self.tray_icon.setToolTip("WDock - Панель швидкого запуску")
        
        return True
    
    def create_tray_icon_pixmap(self) -> QPixmap:
        """Create custom tray icon pixmap using Lucide icons"""
        # Try to use Lucide icon, fallback to custom if not available
        tray_icon = get_wdock_icon("tray_icon", size=16, is_dark=False)
        if tray_icon:
            return tray_icon.pixmap(16, 16)
        
        # Fallback to custom icon
        size = 16
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create a simple dock-like icon
        # Main rectangle (dock base)
        painter.fillRect(2, 10, 12, 4, QBrush(QColor(100, 150, 200)))
        
        # App icons on dock
        icon_colors = [QColor(255, 100, 100), QColor(100, 255, 100), QColor(100, 100, 255)]
        for i, color in enumerate(icon_colors):
            x = 3 + i * 3
            painter.fillRect(x, 8, 2, 2, QBrush(color))
        
        painter.end()
        return pixmap
    
    def create_tray_menu(self):
        """Create the system tray context menu"""
        self.tray_menu = QMenu()
        
        # Detect current theme for proper icon colors
        theme = self.config_manager.get("theme", "auto")
        if theme == "auto":
            # Use dock window theme detection if available
            if self.dock_window:
                is_dark = self.dock_window.is_dark_theme()
            else:
                # Fallback theme detection
                try:
                    import winreg
                    key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER,
                        r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                    )
                    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                    winreg.CloseKey(key)
                    is_dark = value == 0  # 0 = dark theme, 1 = light theme
                except:
                    is_dark = False  # Default to light theme
        else:
            is_dark = theme == "dark"
        
        # Show/Hide dock action
        self.show_hide_action = QAction("Показати док", self)
        show_icon = get_wdock_icon("show_dock", size=16, is_dark=is_dark)
        if show_icon:
            self.show_hide_action.setIcon(show_icon)
        self.show_hide_action.triggered.connect(self.toggle_dock_visibility)
        self.tray_menu.addAction(self.show_hide_action)
        
        self.tray_menu.addSeparator()
        
        # Position submenu
        position_menu = self.tray_menu.addMenu("Прикріпити до")
        
        positions = [
            ("Верх", "top"),
            ("Низ", "bottom"),
            ("Ліво", "left"),
            ("Право", "right")
        ]
        
        self.position_actions = {}
        for text, pos in positions:
            action = QAction(text, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, p=pos: self.change_position(p))
            position_menu.addAction(action)
            self.position_actions[pos] = action
        
        # Update checked position
        current_pos = self.config_manager.get("position", "bottom")
        if current_pos in self.position_actions:
            self.position_actions[current_pos].setChecked(True)
        
        # Auto-hide action
        self.auto_hide_action = QAction("Автоприховування", self)
        self.auto_hide_action.setCheckable(True)
        self.auto_hide_action.setChecked(self.config_manager.get("auto_hide", True))
        self.auto_hide_action.triggered.connect(self.toggle_auto_hide)
        self.tray_menu.addAction(self.auto_hide_action)
        
        # Intelligent hide action
        self.intelligent_hide_action = QAction("Розумне приховування", self)
        self.intelligent_hide_action.setCheckable(True)
        self.intelligent_hide_action.setChecked(self.config_manager.get("intelligent_hide", True))
        self.intelligent_hide_action.triggered.connect(self.toggle_intelligent_hide)
        self.tray_menu.addAction(self.intelligent_hide_action)
        
        self.tray_menu.addSeparator()
        
        # Settings action
        settings_action = QAction("Налаштування...", self)
        settings_icon = get_wdock_icon("settings_main", size=16, is_dark=is_dark)
        if settings_icon:
            settings_action.setIcon(settings_icon)
        settings_action.triggered.connect(self.settings_requested.emit)
        self.tray_menu.addAction(settings_action)
        
        # About action
        about_action = QAction("Про програму...", self)
        about_icon = get_wdock_icon("about", size=16, is_dark=is_dark)
        if about_icon:
            about_action.setIcon(about_icon)
        about_action.triggered.connect(self.about_requested.emit)
        self.tray_menu.addAction(about_action)
        
        self.tray_menu.addSeparator()
        
        # Quit action
        quit_action = QAction("Завершити WDock", self)
        quit_icon = get_wdock_icon("exit_app", size=16, is_dark=is_dark)
        if quit_icon:
            quit_action.setIcon(quit_icon)
        quit_action.triggered.connect(self.quit_requested.emit)
        self.tray_menu.addAction(quit_action)
        
        # Set menu
        if self.tray_icon:
            self.tray_icon.setContextMenu(self.tray_menu)
    
    def setup_connections(self):
        """Setup signal connections"""
        if self.tray_icon:
            # Double-click to toggle dock visibility
            self.tray_icon.activated.connect(self.on_tray_icon_activated)
    
    def on_tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.toggle_dock_visibility()
        elif reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Single click - show dock context menu if dock window is available
            if self.dock_window:
                # Create and show dock context menu at cursor position
                import PyQt6.QtGui as QtGui
                cursor_pos = QtGui.QCursor.pos()
                # Convert to dock window coordinates
                local_pos = self.dock_window.mapFromGlobal(cursor_pos)
                self.dock_window.show_dock_context_menu(local_pos)
            else:
                # Fallback to toggling dock visibility
                self.toggle_dock_visibility()
    
    def toggle_dock_visibility(self):
        """Toggle dock visibility"""
        # This would need to be connected to the dock window
        # For now, emit signal
        self.show_dock_requested.emit()
    
    def change_position(self, position: str):
        """Change dock position"""
        self.config_manager.set("position", position)
        
        # Update checked status
        for pos, action in self.position_actions.items():
            action.setChecked(pos == position)
    
    def toggle_auto_hide(self, checked: bool):
        """Toggle auto-hide setting"""
        self.config_manager.set("auto_hide", checked)
    
    def toggle_intelligent_hide(self, checked: bool):
        """Toggle intelligent hide setting"""
        self.config_manager.set("intelligent_hide", checked)
    
    def show(self):
        """Show the system tray icon"""
        if self.tray_icon:
            self.tray_icon.show()
    
    def hide(self):
        """Hide the system tray icon"""
        if self.tray_icon:
            self.tray_icon.hide()
    
    def show_message(self, title: str, message: str, icon=QSystemTrayIcon.MessageIcon.Information, timeout=3000):
        """Show a system tray notification"""
        if self.tray_icon and self.tray_icon.supportsMessages():
            self.tray_icon.showMessage(title, message, icon, timeout)
    
    def update_dock_status(self, is_visible: bool):
        """Update the show/hide action text and icon based on dock visibility"""
        # Detect current theme for proper icon colors
        theme = self.config_manager.get("theme", "auto")
        if theme == "auto":
            if self.dock_window:
                is_dark = self.dock_window.is_dark_theme()
            else:
                try:
                    import winreg
                    key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER,
                        r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                    )
                    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                    winreg.CloseKey(key)
                    is_dark = value == 0
                except:
                    is_dark = False
        else:
            is_dark = theme == "dark"
        
        if is_visible:
            self.show_hide_action.setText("Приховати док")
            hide_icon = get_wdock_icon("hide_dock", size=16, is_dark=is_dark)
            if hide_icon:
                self.show_hide_action.setIcon(hide_icon)
        else:
            self.show_hide_action.setText("Показати док")
            show_icon = get_wdock_icon("show_dock", size=16, is_dark=is_dark)
            if show_icon:
                self.show_hide_action.setIcon(show_icon)
    
    def update_position_menu(self, current_position: str):
        """Update position menu to reflect current position"""
        for pos, action in self.position_actions.items():
            action.setChecked(pos == current_position)
    
    def is_available(self) -> bool:
        """Check if system tray is available"""
        return QSystemTrayIcon.isSystemTrayAvailable()
    
    def set_dock_window(self, dock_window):
        """Set the dock window reference for context menu integration"""
        self.dock_window = dock_window
    
    def cleanup(self):
        """Cleanup system tray resources"""
        if self.tray_icon:
            self.tray_icon.hide()
            self.tray_icon = None