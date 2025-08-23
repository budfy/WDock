"""
Main Dock Window for WDock
Frameless, transparent, always-on-top window that hosts the dock
"""

import sys
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QApplication, 
                             QGraphicsDropShadowEffect, QFrame, QMenu)
from PyQt6.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QEasingCurve, pyqtSignal, QPoint
from PyQt6.QtGui import QPalette, QColor, QPainter, QBrush, QPen, QAction
import ctypes
from ctypes import wintypes

from .config_manager import ConfigManager
from ..ui.icon_widget import IconWidget
from ..ui.group_widget import GroupWidget
from ..utils.drag_drop import DragDropHelper, DropZoneWidget, GroupDropZone
from ..utils.multi_monitor import get_monitor_manager


class DockWindow(QWidget):
    """Main dock window with frameless design and transparency"""
    
    # Signals
    position_changed = pyqtSignal(str)
    
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self.monitor_manager = get_monitor_manager()
        self.is_hidden = False
        self.auto_hide_timer = QTimer()
        self.hide_animation = None
        self.show_animation = None
        
        # Drop zones for visual feedback
        self.drop_zone = DropZoneWidget(self)
        self.group_zone = GroupDropZone(self)
        self.drop_target_widget = None
        
        self.setup_window()
        self.setup_layout()
        self.setup_animations()
        self.setup_auto_hide()
        self.load_icons()
        self.position_dock()
    
    def setup_window(self):
        """Configure window properties"""
        # Make window frameless and always on top
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # Enable transparency
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        
        # Set window title for identification
        self.setWindowTitle("WDock")
        
        # Set minimum size
        self.setMinimumSize(100, 60)
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        
        # Make window accept drops
        self.setAcceptDrops(True)
    
    def setup_layout(self):
        """Setup the main layout"""
        # Create main container
        self.container = QFrame()
        self.container.setObjectName("dockContainer")
        
        # Get position from config
        position = self.config_manager.get("position", "bottom")
        if position is None:
            position = "bottom"
        
        self.update_layout_for_position(position)
        
        # Main layout for the window
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)
        self.setLayout(main_layout)
        
        # Apply styles
        self.apply_styles()
    
    def update_layout_for_position(self, position: str):
        """Update layout orientation based on position"""
        # Check if layout needs to change
        current_is_horizontal = hasattr(self, 'dock_layout') and isinstance(self.dock_layout, QHBoxLayout)
        new_is_horizontal = position in ["top", "bottom"]
        
        if hasattr(self, 'dock_layout') and (current_is_horizontal == new_is_horizontal):
            # Layout orientation hasn't changed, no need to update
            return
        
        # Save existing widgets
        widgets = []
        if hasattr(self, 'dock_layout') and self.dock_layout:
            while self.dock_layout.count():
                item = self.dock_layout.takeAt(0)
                if item.widget():
                    widgets.append(item.widget())
        
        # Create appropriate layout for position
        if position in ["top", "bottom"]:
            self.dock_layout = QHBoxLayout()
            self.setFixedHeight(60)
            self.setMaximumWidth(16777215)  # Remove width constraint
        else:  # left, right
            self.dock_layout = QVBoxLayout()
            self.setFixedWidth(60)
            self.setMaximumHeight(16777215)  # Remove height constraint
        
        self.dock_layout.setContentsMargins(8, 8, 8, 8)
        self.dock_layout.setSpacing(4)
        
        # Only set layout if container doesn't have one
        if not self.container.layout():
            self.container.setLayout(self.dock_layout)
        else:
            # Replace the existing layout
            old_layout = self.container.layout()
            old_layout.deleteLater()
            self.container.setLayout(self.dock_layout)
        
        # Restore widgets
        for widget in widgets:
            self.dock_layout.addWidget(widget)
    
    def apply_styles(self):
        """Apply CSS styles to the dock"""
        # Determine theme
        theme = self.config_manager.get("theme", "auto")
        if theme == "auto":
            # Detect Windows theme automatically
            is_dark = self.is_dark_theme()
        else:
            is_dark = theme == "dark"
        
        if is_dark:
            bg_color = "rgba(40, 40, 40, 200)"
            border_color = "rgba(80, 80, 80, 150)"
        else:
            bg_color = "rgba(240, 240, 240, 200)"
            border_color = "rgba(200, 200, 200, 150)"
        
        style = f"""
        QFrame#dockContainer {{
            background-color: {bg_color};
            border: 1px solid {border_color};
            border-radius: 12px;
        }}
        """
        
        self.container.setStyleSheet(style)
        
        # Add drop shadow effect with reduced blur to avoid coordinate issues
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)  # Reduced from 20 to avoid positioning issues
        shadow.setXOffset(0)
        shadow.setYOffset(1)      # Reduced from 2
        shadow.setColor(QColor(0, 0, 0, 40))  # Reduced opacity from 60
        self.container.setGraphicsEffect(shadow)
    
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
    
    def setup_animations(self):
        """Setup show/hide animations"""
        self.hide_animation = QPropertyAnimation(self, b"geometry")
        self.hide_animation.setDuration(200)
        self.hide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.show_animation = QPropertyAnimation(self, b"geometry")
        self.show_animation.setDuration(200)
        self.show_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def setup_auto_hide(self):
        """Setup auto-hide functionality"""
        if self.config_manager.get("auto_hide", True):
            self.auto_hide_timer.timeout.connect(self.check_auto_hide)
            self.auto_hide_timer.start(500)  # Check every 500ms
    
    def check_auto_hide(self):
        """Check if dock should auto-hide"""
        if not self.config_manager.get("auto_hide", True):
            return
        
        # Get cursor position
        cursor_pos = self.mapFromGlobal(self.cursor().pos())
        is_cursor_over = self.rect().contains(cursor_pos)
        
        # Check if intelligent hide is enabled
        if self.config_manager.get("intelligent_hide", True):
            if self.is_fullscreen_app_active():
                if not self.is_hidden:
                    self.hide_dock()
                return
        
        # Normal auto-hide behavior
        if not is_cursor_over and not self.is_hidden:
            self.hide_dock()
        elif is_cursor_over and self.is_hidden:
            self.show_dock()
    
    def is_fullscreen_app_active(self) -> bool:
        """Check if a fullscreen application is active"""
        try:
            # Get foreground window
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            
            if not hwnd:
                return False
            
            # Get window rect
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            
            # Get screen dimensions
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            
            # Check if window covers entire screen
            window_width = rect.right - rect.left
            window_height = rect.bottom - rect.top
            
            return (window_width >= screen_width and 
                    window_height >= screen_height and
                    rect.left <= 0 and rect.top <= 0)
        except:
            return False
    
    def get_work_area(self) -> QRect:
        """Get the work area (screen minus taskbar)"""
        # Use multi-monitor manager for better work area detection
        return self.monitor_manager.get_work_area()
    
    def position_dock(self):
        """Position the dock according to configuration"""
        position = self.config_manager.get("position", "bottom")
        alignment = self.config_manager.get("alignment", "center")
        
        # Ensure position and alignment are not None
        if position is None:
            position = "bottom"
        if alignment is None:
            alignment = "center"
        
        # Update layout orientation if position changed
        self.update_layout_for_position(position)
        
        work_area = self.get_work_area()
        
        if position == "bottom":
            self.position_bottom(work_area, alignment)
        elif position == "top":
            self.position_top(work_area, alignment)
        elif position == "left":
            self.position_left(work_area, alignment)
        elif position == "right":
            self.position_right(work_area, alignment)
        
        self.position_changed.emit(position)
    
    def calculate_dock_size(self, position: str) -> tuple:
        """Calculate appropriate dock size based on content and position"""
        icon_count = max(1, self.dock_layout.count() if hasattr(self, 'dock_layout') else 1)  # At least 1 to avoid zero width
        icon_size = 48
        margin = 16  # Total margins (8 on each side)
        spacing = 4
        
        if position in ["top", "bottom"]:
            # Horizontal layout
            width = (icon_count * icon_size) + ((icon_count - 1) * spacing) + margin
            width = max(200, min(width, 800))  # Reasonable bounds
            height = 60
        else:
            # Vertical layout (left, right)
            width = 60
            height = (icon_count * icon_size) + ((icon_count - 1) * spacing) + margin
            height = max(200, min(height, 600))  # Reasonable bounds
        
        return width, height
    
    def position_bottom(self, work_area: QRect, alignment: str):
        """Position dock at bottom"""
        dock_width, dock_height = self.calculate_dock_size("bottom")
        
        if alignment == "start":  # Left edge
            x = work_area.left() + 10
        elif alignment == "end":  # Right edge
            x = work_area.right() - dock_width - 10
        else:  # center
            x = work_area.center().x() - dock_width // 2
        
        # Ensure dock stays within screen bounds
        x = max(work_area.left(), min(x, work_area.right() - dock_width))
        y = work_area.bottom() - dock_height - 10
        
        self.setGeometry(x, y, dock_width, dock_height)
    
    def position_top(self, work_area: QRect, alignment: str):
        """Position dock at top"""
        dock_width, dock_height = self.calculate_dock_size("top")
        
        if alignment == "start":  # Left edge
            x = work_area.left() + 10
        elif alignment == "end":  # Right edge
            x = work_area.right() - dock_width - 10
        else:  # center
            x = work_area.center().x() - dock_width // 2
        
        # Ensure dock stays within screen bounds
        x = max(work_area.left(), min(x, work_area.right() - dock_width))
        y = work_area.top() + 10
        
        self.setGeometry(x, y, dock_width, dock_height)
    
    def position_left(self, work_area: QRect, alignment: str):
        """Position dock at left"""
        dock_width, dock_height = self.calculate_dock_size("left")
        
        x = work_area.left() + 10
        
        if alignment == "start":  # Top edge
            y = work_area.top() + 10
        elif alignment == "end":  # Bottom edge
            y = work_area.bottom() - dock_height - 10
        else:  # center
            y = work_area.center().y() - dock_height // 2
        
        # Ensure dock stays within screen bounds
        y = max(work_area.top(), min(y, work_area.bottom() - dock_height))
        
        self.setGeometry(x, y, dock_width, dock_height)
    
    def position_right(self, work_area: QRect, alignment: str):
        """Position dock at right"""
        dock_width, dock_height = self.calculate_dock_size("right")
        
        x = work_area.right() - dock_width - 10
        
        if alignment == "start":  # Top edge
            y = work_area.top() + 10
        elif alignment == "end":  # Bottom edge
            y = work_area.bottom() - dock_height - 10
        else:  # center
            y = work_area.center().y() - dock_height // 2
        
        # Ensure dock stays within screen bounds
        y = max(work_area.top(), min(y, work_area.bottom() - dock_height))
        
        self.setGeometry(x, y, dock_width, dock_height)
    
    def hide_dock(self):
        """Hide the dock with animation"""
        if self.is_hidden:
            return
        
        self.is_hidden = True
        position = self.config_manager.get("position", "bottom")
        current_geo = self.geometry()
        
        if position == "bottom":
            target_geo = QRect(current_geo.x(), current_geo.y() + current_geo.height() - 5,
                              current_geo.width(), current_geo.height())
        elif position == "top":
            target_geo = QRect(current_geo.x(), current_geo.y() - current_geo.height() + 5,
                              current_geo.width(), current_geo.height())
        elif position == "left":
            target_geo = QRect(current_geo.x() - current_geo.width() + 5, current_geo.y(),
                              current_geo.width(), current_geo.height())
        else:  # right
            target_geo = QRect(current_geo.x() + current_geo.width() - 5, current_geo.y(),
                              current_geo.width(), current_geo.height())
        
        self.hide_animation.setStartValue(current_geo)
        self.hide_animation.setEndValue(target_geo)
        self.hide_animation.start()
    
    def show_dock(self):
        """Show the dock with animation"""
        if not self.is_hidden:
            return
        
        self.is_hidden = False
        current_geo = self.geometry()
        
        # Calculate target position
        work_area = self.get_work_area()
        position = self.config_manager.get("position", "bottom")
        alignment = self.config_manager.get("alignment", "center")
        
        # Ensure position and alignment are not None
        if position is None:
            position = "bottom"
        if alignment is None:
            alignment = "center"
        
        if position == "bottom":
            self.position_bottom(work_area, alignment)
        elif position == "top":
            self.position_top(work_area, alignment)
        elif position == "left":
            self.position_left(work_area, alignment)
        elif position == "right":
            self.position_right(work_area, alignment)
        
        target_geo = self.geometry()
        self.setGeometry(current_geo)  # Reset to hidden position
        
        self.show_animation.setStartValue(current_geo)
        self.show_animation.setEndValue(target_geo)
        self.show_animation.start()
    
    def enterEvent(self, event):
        """Mouse entered dock area"""
        if self.is_hidden:
            self.show_dock()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Mouse left dock area"""
        super().leaveEvent(event)
    
    def contextMenuEvent(self, event):
        """Handle right-click context menu"""
        self.show_dock_context_menu(event.pos())
    
    def show_dock_context_menu(self, position: QPoint):
        """Show the dock context menu"""
        menu = QMenu(self)
        
        # Import here to avoid circular imports
        from ..utils.lucide_icons import get_wdock_icon
        
        # Detect current theme for proper icon colors
        theme = self.config_manager.get("theme", "auto")
        if theme == "auto":
            is_dark = self.is_dark_theme()
        else:
            is_dark = theme == "dark"
        
        # Position submenu
        position_menu = menu.addMenu("Прикріпити до")
        
        positions = [
            ("Верх", "top"),
            ("Низ", "bottom"),
            ("Ліво", "left"),
            ("Право", "right")
        ]
        
        current_pos = self.config_manager.get("position", "bottom")
        for text, pos in positions:
            action = QAction(text, self)
            action.setCheckable(True)
            action.setChecked(pos == current_pos)
            action.triggered.connect(lambda checked, p=pos: self.change_dock_position(p))
            position_menu.addAction(action)
        
        # Alignment submenu
        alignment_menu = menu.addMenu("Вирівнювання")
        
        alignments = [
            ("Ліво/Верх", "start"),
            ("По центру", "center"),
            ("Право/Низ", "end")
        ]
        
        current_align = self.config_manager.get("alignment", "center")
        for text, align in alignments:
            action = QAction(text, self)
            action.setCheckable(True)
            action.setChecked(align == current_align)
            action.triggered.connect(lambda checked, a=align: self.change_dock_alignment(a))
            alignment_menu.addAction(action)
        
        menu.addSeparator()
        
        # Auto-hide action
        auto_hide_action = QAction("Автоприховування", self)
        auto_hide_action.setCheckable(True)
        auto_hide_value = self.config_manager.get("auto_hide", True)
        auto_hide_action.setChecked(bool(auto_hide_value) if auto_hide_value is not None else True)
        auto_hide_action.triggered.connect(self.toggle_auto_hide)
        menu.addAction(auto_hide_action)
        
        # Intelligent hide action
        intelligent_hide_action = QAction("Розумне приховування", self)
        intelligent_hide_action.setCheckable(True)
        intelligent_hide_value = self.config_manager.get("intelligent_hide", True)
        intelligent_hide_action.setChecked(bool(intelligent_hide_value) if intelligent_hide_value is not None else True)
        intelligent_hide_action.triggered.connect(self.toggle_intelligent_hide)
        menu.addAction(intelligent_hide_action)
        
        menu.addSeparator()
        
        # Settings action
        settings_action = QAction("Налаштування...", self)
        settings_icon = get_wdock_icon("settings_main", size=16, is_dark=is_dark)
        if settings_icon:
            settings_action.setIcon(settings_icon)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)
        
        # About action
        about_action = QAction("Про програму...", self)
        about_icon = get_wdock_icon("about", size=16, is_dark=is_dark)
        if about_icon:
            about_action.setIcon(about_icon)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)
        
        menu.addSeparator()
        
        # Quit action
        quit_action = QAction("Завершити WDock", self)
        quit_icon = get_wdock_icon("exit_app", size=16, is_dark=is_dark)
        if quit_icon:
            quit_action.setIcon(quit_icon)
        quit_action.triggered.connect(self.quit_application)
        menu.addAction(quit_action)
        
        # Show menu
        global_pos = self.mapToGlobal(position)
        menu.exec(global_pos)
    
    def dragEnterEvent(self, event):
        """Handle drag enter events"""
        if (event.mimeData().hasUrls() or 
            DragDropHelper.is_wdock_icon_drag(event.mimeData())):
            event.acceptProposedAction()
            self.show_drop_zones(event.position().toPoint())
        super().dragEnterEvent(event)
    
    def dragMoveEvent(self, event):
        """Handle drag move events"""
        if (event.mimeData().hasUrls() or 
            DragDropHelper.is_wdock_icon_drag(event.mimeData())):
            self.update_drop_zones(event.position().toPoint())
            event.acceptProposedAction()
        super().dragMoveEvent(event)
    
    def dragLeaveEvent(self, event):
        """Handle drag leave events"""
        self.hide_drop_zones()
        super().dragLeaveEvent(event)
    
    def dropEvent(self, event):
        """Handle drop events"""
        self.hide_drop_zones()
        
        if DragDropHelper.is_wdock_icon_drag(event.mimeData()):
            # Handle internal icon drag (for grouping)
            icon_data = DragDropHelper.extract_icon_data(event.mimeData())
            if icon_data and self.drop_target_widget:
                self.handle_icon_group(icon_data, self.drop_target_widget)
        
        elif event.mimeData().hasUrls():
            # Handle external file drops
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith(('.lnk', '.exe')):
                    self.add_icon_to_dock(file_path)
        
        event.acceptProposedAction()
        self.drop_target_widget = None
        super().dropEvent(event)
    
    def load_icons(self):
        """Load icons from configuration"""
        icons = self.config_manager.get_icons()
        groups = self.config_manager.get_groups()
        
        # Clear existing icons
        self.clear_layout()
        
        # Group icons by group membership
        grouped_icons = {}
        ungrouped_icons = []
        
        for icon_data in icons:
            group_name = icon_data.get("group")
            if group_name and group_name in groups:
                if group_name not in grouped_icons:
                    grouped_icons[group_name] = []
                grouped_icons[group_name].append(icon_data)
            else:
                ungrouped_icons.append(icon_data)
        
        # Add ungrouped icons
        for icon_data in ungrouped_icons:
            self.add_icon_widget(icon_data)
        
        # Add grouped icons
        for group_name, group_icons in grouped_icons.items():
            group_data = groups[group_name]
            self.add_group_widget(group_data, group_icons)
    
    def clear_layout(self):
        """Clear all widgets from the layout"""
        if hasattr(self, 'dock_layout'):
            while self.dock_layout.count():
                child = self.dock_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
    
    def add_icon_to_dock(self, file_path: str, name: str = None):
        """Add a new icon to the dock"""
        self.config_manager.add_icon(file_path, name)
        self.load_icons()  # Reload to refresh display
    
    def add_icon_widget(self, icon_data: dict):
        """Add an icon widget to the layout"""
        icon_widget = IconWidget(icon_data, self)
        if hasattr(self, 'dock_layout'):
            self.dock_layout.addWidget(icon_widget)
        return icon_widget
    
    def add_group_widget(self, group_data: dict, icons: list):
        """Add a group widget to the layout"""
        group_widget = GroupWidget(group_data, icons, self)
        if hasattr(self, 'dock_layout'):
            self.dock_layout.addWidget(group_widget)
        return group_widget
    
    def remove_icon_widget(self, icon_widget):
        """Remove an icon widget from the dock"""
        icon_path = icon_widget.icon_data.get("path")
        if icon_path:
            self.config_manager.remove_icon(icon_path)
        
        if hasattr(self, 'dock_layout'):
            self.dock_layout.removeWidget(icon_widget)
        icon_widget.deleteLater()
        
        # Reposition dock if needed
        self.position_dock()
    
    def show_drop_zones(self, pos: QPoint):
        """Show drop zones for visual feedback"""
        # Find widget under cursor
        widget = self.childAt(pos)
        
        if isinstance(widget, (IconWidget, GroupWidget)):
            # Show group creation zone
            widget_geo = widget.geometry()
            self.group_zone.show_group_zone(widget_geo)
            self.drop_target_widget = widget
        else:
            # Show general drop zone
            drop_rect = QRect(pos.x() - 32, pos.y() - 32, 64, 64)
            self.drop_zone.show_drop_zone(drop_rect)
    
    def update_drop_zones(self, pos: QPoint):
        """Update drop zone positions during drag"""
        widget = self.childAt(pos)
        
        if isinstance(widget, (IconWidget, GroupWidget)):
            if widget != self.drop_target_widget:
                self.drop_zone.hide_drop_zone()
                widget_geo = widget.geometry()
                self.group_zone.show_group_zone(widget_geo)
                self.drop_target_widget = widget
        else:
            self.group_zone.hide_group_zone()
            self.drop_target_widget = None
            drop_rect = QRect(pos.x() - 32, pos.y() - 32, 64, 64)
            self.drop_zone.show_drop_zone(drop_rect)
    
    def hide_drop_zones(self):
        """Hide all drop zones"""
        self.drop_zone.hide_drop_zone()
        self.group_zone.hide_group_zone()
        self.drop_target_widget = None
    
    def handle_icon_group(self, dragged_icon_data: dict, target_widget):
        """Handle grouping of icons"""
        if isinstance(target_widget, IconWidget):
            # Create new group with two icons
            self.create_group_from_icons(dragged_icon_data, target_widget.icon_data)
        elif isinstance(target_widget, GroupWidget):
            # Add to existing group
            self.add_icon_to_group(dragged_icon_data, target_widget)
    
    def create_group_from_icons(self, icon1_data: dict, icon2_data: dict):
        """Create a new group from two icons"""
        from PyQt6.QtWidgets import QInputDialog
        
        # Ask for group name
        group_name, ok = QInputDialog.getText(
            self, "Нова група", "Назва групи:", 
            text="Група"
        )
        
        if ok and group_name.strip():
            # Create group in config
            self.config_manager.add_group(group_name.strip())
            
            # Update icons to belong to group
            for icon in self.config_manager.get_icons():
                if (icon.get("path") == icon1_data.get("path") or 
                    icon.get("path") == icon2_data.get("path")):
                    icon["group"] = group_name.strip()
            
            self.config_manager.save_config()
            self.load_icons()  # Reload to show group
    
    def add_icon_to_group(self, icon_data: dict, group_widget: GroupWidget):
        """Add an icon to an existing group"""
        group_name = None
        for name, data in self.config_manager.get_groups().items():
            if data == group_widget.group_data:
                group_name = name
                break
        
        if group_name:
            # Update icon to belong to group
            for icon in self.config_manager.get_icons():
                if icon.get("path") == icon_data.get("path"):
                    icon["group"] = group_name
                    break
            
            self.config_manager.save_config()
            self.load_icons()  # Reload to update display
    
    def change_dock_position(self, position: str):
        """Change dock position"""
        self.config_manager.set("position", position)
        self.position_dock()
        self.position_changed.emit(position)
    
    def change_dock_alignment(self, alignment: str):
        """Change dock alignment"""
        self.config_manager.set("alignment", alignment)
        self.position_dock()
    
    def toggle_auto_hide(self, checked: bool):
        """Toggle auto-hide setting"""
        self.config_manager.set("auto_hide", checked)
        if checked:
            self.setup_auto_hide()
        else:
            self.auto_hide_timer.stop()
    
    def toggle_intelligent_hide(self, checked: bool):
        """Toggle intelligent hide setting"""
        self.config_manager.set("intelligent_hide", checked)
    
    def show_settings(self):
        """Show settings window"""
        # Import here to avoid circular imports
        from ..ui.settings_window import SettingsWindow
        
        settings_window = SettingsWindow(self.config_manager, self)
        settings_window.position_changed.connect(self.position_dock)
        settings_window.settings_changed.connect(self.load_icons)
        settings_window.exec()
    
    def show_about(self):
        """Show about window"""
        # Import here to avoid circular imports
        from ..ui.about_window import AboutWindow
        
        about_window = AboutWindow(self)
        about_window.exec()
    
    def quit_application(self):
        """Quit the application"""
        QApplication.quit()