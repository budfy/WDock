"""
Icon Widget for WDock
Displays application icons with hover effects and animations
"""

import os
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QMenu, 
                             QGraphicsDropShadowEffect, QGraphicsOpacityEffect)
from PyQt6.QtCore import (Qt, QTimer, QPropertyAnimation, QEasingCurve, 
                          QRect, pyqtSignal, QPoint, QSize)
from PyQt6.QtGui import (QPixmap, QIcon, QAction, QPainter, QPen, QBrush, 
                         QColor, QFont, QFontMetrics, QPainterPath)
import win32api
import win32gui
from PIL import Image, ImageDraw

from ..utils.drag_drop import DragDropHelper


class IconWidget(QWidget):
    """Widget representing a single application icon in the dock"""
    
    # Signals
    clicked = pyqtSignal()
    right_clicked = pyqtSignal()
    drag_started = pyqtSignal()
    
    def __init__(self, icon_data: dict, parent=None):
        super().__init__(parent)
        self.icon_data = icon_data
        self.icon_size = 48  # Default size
        self.is_hovered = False
        self.is_pressed = False
        self.drag_start_position = None
        
        # Animation properties
        self.hover_animation = None
        self.press_animation = None
        self.bounce_animation = None
        
        # UI elements
        self.icon_label = None
        self.name_label = None
        
        self.setup_ui()
        self.setup_animations()
        self.load_icon()
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
    
    def setup_ui(self):
        """Setup the user interface"""
        self.setFixedSize(64, 64)  # Padding around 48px icon
        
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(2)
        
        # Icon label
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setScaledContents(False)
        layout.addWidget(self.icon_label)
        
        # Name label (optional, for tooltip-style display)
        self.name_label = QLabel(self.icon_data.get("name", ""))
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setVisible(False)  # Hidden by default
        font = self.name_label.font()
        font.setPointSize(8)
        self.name_label.setFont(font)
        layout.addWidget(self.name_label)
        
        self.setLayout(layout)
        
        # Set tooltip
        self.setToolTip(self.icon_data.get("name", ""))
        # Enable context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def setup_animations(self):
        """Setup hover and click animations"""
        # Hover animation (scale effect)
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(150)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # Press animation
        self.press_animation = QPropertyAnimation(self, b"geometry")
        self.press_animation.setDuration(100)
        self.press_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # Bounce animation for launch
        self.bounce_animation = QPropertyAnimation(self, b"geometry")
        self.bounce_animation.setDuration(300)
        self.bounce_animation.setEasingCurve(QEasingCurve.Type.OutBounce)
    
    def load_icon(self):
        """Load and set the application icon"""
        icon_path = self.icon_data.get("path", "")
        
        if not icon_path or not os.path.exists(icon_path):
            # Use default icon
            print(f"Icon path invalid or doesn't exist: {icon_path}")
            self.set_default_icon()
            return
        
        try:
            if icon_path.endswith('.lnk'):
                icon_pixmap = self.extract_shortcut_icon(icon_path)
            elif icon_path.endswith('.exe'):
                icon_pixmap = self.extract_exe_icon(icon_path)
            else:
                # Try to load as image file
                icon_pixmap = QPixmap(icon_path)
            
            if icon_pixmap and not icon_pixmap.isNull():
                # Scale to appropriate size with smooth transformation
                scaled_pixmap = icon_pixmap.scaled(
                    self.icon_size, self.icon_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.icon_label.setPixmap(scaled_pixmap)
                print(f"Successfully loaded icon for {self.icon_data.get('name', 'Unknown')}")
            else:
                print(f"Failed to extract icon for {self.icon_data.get('name', 'Unknown')}, using default")
                self.set_default_icon()
                
        except Exception as e:
            print(f"Error loading icon for {icon_path}: {e}")
            self.set_default_icon()
    
    def extract_shortcut_icon(self, lnk_path: str) -> QPixmap:
        """Extract icon from .lnk shortcut file"""
        # Method 1: Try QFileIconProvider first (most reliable for shortcuts)
        try:
            from PyQt6.QtWidgets import QFileIconProvider
            from PyQt6.QtCore import QFileInfo
            
            provider = QFileIconProvider()
            file_info = QFileInfo(lnk_path)
            icon = provider.icon(file_info)
            
            if not icon.isNull():
                available_sizes = icon.availableSizes()
                if available_sizes:
                    largest_size = max(available_sizes, key=lambda s: s.width() * s.height())
                    pixmap = icon.pixmap(largest_size)
                    
                    if not pixmap.isNull() and pixmap.width() > 16:  # Ensure it's not just a tiny generic icon
                        return pixmap.scaled(
                            self.icon_size, self.icon_size,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
        except Exception as e:
            print(f"QFileIconProvider shortcut method failed: {e}")
        
        # Method 2: Extract target path and get icon from target
        try:
            import pythoncom
            from win32com.shell import shell, shellcon
            
            shortcut = pythoncom.CoCreateInstance(
                shell.CLSID_ShellLink,
                None,
                pythoncom.CLSCTX_INPROC_SERVER,
                shell.IID_IShellLink
            )
            
            shortcut.QueryInterface(pythoncom.IID_IPersistFile).Load(lnk_path)
            
            # Get target path and extract icon from it
            target_path, _ = shortcut.GetPath(shell.SLGP_SHORTPATH)
            if target_path and os.path.exists(target_path):
                return self.extract_exe_icon(target_path)
            
        except Exception as e:
            print(f"Error extracting shortcut icon: {e}")
        
        # Method 3: Fallback to app-style icon
        return self.create_app_style_icon(lnk_path)
    
    def extract_exe_icon(self, exe_path: str) -> QPixmap:
        """Extract icon from executable file using multiple fallback methods"""
        # Method 1: Try using QFileIconProvider (most reliable)
        try:
            from PyQt6.QtWidgets import QFileIconProvider
            from PyQt6.QtCore import QFileInfo
            
            provider = QFileIconProvider()
            file_info = QFileInfo(exe_path)
            icon = provider.icon(file_info)
            
            if not icon.isNull():
                # Get the largest available size
                available_sizes = icon.availableSizes()
                if available_sizes:
                    # Use the largest available size
                    largest_size = max(available_sizes, key=lambda s: s.width() * s.height())
                    pixmap = icon.pixmap(largest_size)
                    
                    if not pixmap.isNull():
                        return pixmap.scaled(
                            self.icon_size, self.icon_size,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
        except Exception as e:
            print(f"QFileIconProvider method failed: {e}")
        
        # Method 2: Try Windows API with PIL conversion
        try:
            large_icons, small_icons = win32gui.ExtractIconEx(exe_path, 0)
            
            if large_icons:
                icon_handle = large_icons[0]
                
                # Get icon info
                icon_info = win32gui.GetIconInfo(icon_handle)
                
                # Try to create a bitmap and convert to PIL Image
                try:
                    import win32ui
                    import win32con
                    from PIL import Image, ImageQt
                    
                    # Create device context
                    dc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
                    mem_dc = dc.CreateCompatibleDC()
                    
                    # Create bitmap
                    bitmap = win32ui.CreateBitmap()
                    bitmap.CreateCompatibleBitmap(dc, self.icon_size, self.icon_size)
                    mem_dc.SelectObject(bitmap)
                    
                    # Fill with white background
                    mem_dc.FillSolidRect((0, 0, self.icon_size, self.icon_size), 0xFFFFFF)
                    
                    # Draw icon
                    win32gui.DrawIconEx(
                        mem_dc.GetSafeHdc(), 0, 0, icon_handle,
                        self.icon_size, self.icon_size, 0, None, win32con.DI_NORMAL
                    )
                    
                    # Get bitmap bits
                    bmp_info = bitmap.GetInfo()
                    bmp_str = bitmap.GetBitmapBits(True)
                    
                    # Convert to PIL Image
                    img = Image.frombuffer(
                        'RGB',
                        (bmp_info['bmWidth'], bmp_info['bmHeight']),
                        bmp_str, 'raw', 'BGRX', 0, 1
                    )
                    
                    # Convert PIL Image to QPixmap
                    pixmap = QPixmap.fromImage(ImageQt.ImageQt(img))
                    
                    # Clean up
                    mem_dc.DeleteDC()
                    dc.DeleteDC()
                    win32gui.ReleaseDC(0, win32gui.GetDC(0))
                    
                    if not pixmap.isNull():
                        # Clean up handles
                        for icon_handle in large_icons:
                            win32gui.DestroyIcon(icon_handle)
                        for icon_handle in small_icons:
                            win32gui.DestroyIcon(icon_handle)
                        return pixmap
                        
                except Exception as e:
                    print(f"PIL conversion method failed: {e}")
                
                # Clean up handles
                for icon_handle in large_icons:
                    win32gui.DestroyIcon(icon_handle)
                for icon_handle in small_icons:
                    win32gui.DestroyIcon(icon_handle)
                
        except Exception as e:
            print(f"Windows API method failed: {e}")
        
        # Method 3: Create an application-style icon as fallback
        return self.create_app_style_icon(exe_path)
    
    def create_app_style_icon(self, file_path: str) -> QPixmap:
        """Create a more sophisticated application-style icon"""
        pixmap = QPixmap(self.icon_size, self.icon_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw a rounded square background
        rect = QRect(2, 2, self.icon_size - 4, self.icon_size - 4)
        path = QPainterPath()
        from PyQt6.QtCore import QRectF
        path.addRoundedRect(QRectF(rect), 8, 8)
        
        # Use a nice gradient based on file name
        file_name = os.path.basename(file_path).lower()
        hash_value = hash(file_name) % 7
        
        colors = [
            QColor(76, 175, 80),   # Green
            QColor(33, 150, 243),  # Blue
            QColor(255, 152, 0),   # Orange
            QColor(156, 39, 176),  # Purple
            QColor(244, 67, 54),   # Red
            QColor(0, 188, 212),   # Cyan
            QColor(255, 193, 7),   # Yellow
        ]
        
        color = colors[hash_value]
        painter.fillPath(path, QBrush(color))
        
        # Draw border
        painter.setPen(QPen(color.darker(120), 2))
        painter.drawPath(path)
        
        # Draw application icon symbol (gear/cog)
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.setBrush(QBrush(Qt.GlobalColor.white))
        
        # Draw a simple app symbol
        center_x = self.icon_size // 2
        center_y = self.icon_size // 2
        
        # Draw a window-like symbol
        inner_rect = QRect(center_x - 8, center_y - 8, 16, 16)
        painter.fillRect(inner_rect, QBrush(Qt.GlobalColor.white))
        painter.setPen(QPen(color, 1))
        painter.drawRect(inner_rect)
        
        # Draw title bar
        title_rect = QRect(center_x - 8, center_y - 8, 16, 4)
        painter.fillRect(title_rect, QBrush(color))
        
        painter.end()
        return pixmap
    
    def create_generic_icon(self) -> QPixmap:
        """Create a generic application icon"""
        pixmap = QPixmap(self.icon_size, self.icon_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw rounded rectangle
        rect = QRect(4, 4, self.icon_size - 8, self.icon_size - 8)
        path = QPainterPath()
        # Convert QRect to QRectF for PyQt6 compatibility
        from PyQt6.QtCore import QRectF
        path.addRoundedRect(QRectF(rect), 8, 8)
        
        # Fill with gradient
        painter.fillPath(path, QBrush(QColor(100, 150, 200)))
        
        # Draw border
        painter.setPen(QPen(QColor(70, 120, 170), 2))
        painter.drawPath(path)
        
        # Draw application text
        painter.setPen(QPen(Qt.GlobalColor.white))
        font = QFont("Segoe UI", 8, QFont.Weight.Bold)
        painter.setFont(font)
        
        app_name = self.icon_data.get("name", "App")[:3].upper()
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, app_name)
        
        painter.end()
        return pixmap
    
    def set_default_icon(self):
        """Set a default icon"""
        default_pixmap = self.create_generic_icon()
        self.icon_label.setPixmap(default_pixmap)
    
    def enterEvent(self, event):
        """Handle mouse enter (hover start)"""
        self.is_hovered = True
        self.animate_hover(True)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave (hover end)"""
        self.is_hovered = False
        self.animate_hover(False)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_pressed = True
            self.drag_start_position = event.position().toPoint()
            self.animate_press(True)
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for drag operations"""
        if (event.buttons() == Qt.MouseButton.LeftButton and 
            self.drag_start_position and
            (event.position().toPoint() - self.drag_start_position).manhattanLength() > 10):
            
            # Start drag operation
            self.drag_started.emit()
            result = DragDropHelper.start_icon_drag(self, self.icon_data)
            
            # Reset state after drag
            self.is_pressed = False
            self.drag_start_position = None
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_pressed:
            self.is_pressed = False
            self.drag_start_position = None
            self.animate_press(False)
            
            # Only launch if we didn't drag
            if self.rect().contains(event.position().toPoint()):
                self.launch_application()
                self.clicked.emit()
        
        elif event.button() == Qt.MouseButton.RightButton:
            # Show context menu on right-click
            self.show_context_menu(event.position().toPoint())
            self.right_clicked.emit()
        
        super().mouseReleaseEvent(event)
    
    def animate_hover(self, entering: bool):
        """Animate hover effect"""
        if not self.hover_animation:
            return
        
        current_geo = self.geometry()
        
        if entering:
            # Scale up slightly
            margin = 2
            target_geo = QRect(
                current_geo.x() - margin,
                current_geo.y() - margin,
                current_geo.width() + 2 * margin,
                current_geo.height() + 2 * margin
            )
        else:
            # Scale back to normal
            margin = 2
            target_geo = QRect(
                current_geo.x() + margin,
                current_geo.y() + margin,
                current_geo.width() - 2 * margin,
                current_geo.height() - 2 * margin
            )
        
        self.hover_animation.setStartValue(current_geo)
        self.hover_animation.setEndValue(target_geo)
        self.hover_animation.start()
    
    def animate_press(self, pressing: bool):
        """Animate press effect"""
        if not self.press_animation:
            return
        
        current_geo = self.geometry()
        
        if pressing:
            # Scale down slightly
            margin = 1
            target_geo = QRect(
                current_geo.x() + margin,
                current_geo.y() + margin,
                current_geo.width() - 2 * margin,
                current_geo.height() - 2 * margin
            )
        else:
            # Scale back
            margin = 1
            target_geo = QRect(
                current_geo.x() - margin,
                current_geo.y() - margin,
                current_geo.width() + 2 * margin,
                current_geo.height() + 2 * margin
            )
        
        self.press_animation.setStartValue(current_geo)
        self.press_animation.setEndValue(target_geo)
        self.press_animation.start()
    
    def animate_bounce(self):
        """Animate bounce effect when launching"""
        if not self.bounce_animation:
            return
        
        current_geo = self.geometry()
        
        # Create a sequence: up -> down -> up -> normal
        self.bounce_animation.setStartValue(current_geo)
        
        # Move up slightly
        bounce_geo = QRect(
            current_geo.x(),
            current_geo.y() - 8,
            current_geo.width(),
            current_geo.height()
        )
        self.bounce_animation.setEndValue(bounce_geo)
        
        def return_to_normal():
            self.bounce_animation.setStartValue(bounce_geo)
            self.bounce_animation.setEndValue(current_geo)
            self.bounce_animation.finished.disconnect()
            self.bounce_animation.start()
        
        self.bounce_animation.finished.connect(return_to_normal)
        self.bounce_animation.start()
    
    def launch_application(self):
        """Launch the application associated with this icon"""
        try:
            app_path = self.icon_data.get("path", "")
            if not app_path:
                return
            
            # Animate launch
            self.animate_bounce()
            
            # Launch application
            if app_path.endswith('.lnk'):
                # Launch shortcut
                os.startfile(app_path)
            elif app_path.endswith('.exe'):
                # Launch executable
                subprocess.Popen([app_path], cwd=os.path.dirname(app_path))
            else:
                # Try to open with default program
                os.startfile(app_path)
                
        except Exception as e:
            print(f"Error launching application: {e}")
    
    def show_context_menu(self, position: QPoint):
        """Show context menu for the icon"""
        menu = QMenu(self)
        
        # Import here to avoid circular imports
        from ..utils.lucide_icons import get_wdock_icon
        
        # Get dock window to detect current theme
        dock_window = self.get_dock_window()
        is_dark = False
        if dock_window:
            theme = dock_window.config_manager.get("theme", "auto")
            if theme == "auto":
                is_dark = dock_window.is_dark_theme()
            else:
                is_dark = theme == "dark"
        
        # Open action
        open_action = QAction("Відкрити", self)
        open_icon = get_wdock_icon("home", size=16, is_dark=is_dark)
        if open_icon:
            open_action.setIcon(open_icon)
        open_action.triggered.connect(self.launch_application)
        menu.addAction(open_action)
        
        menu.addSeparator()
        
        # Rename action
        rename_action = QAction("Перейменувати", self)
        rename_icon = get_wdock_icon("edit_app", size=16, is_dark=is_dark)
        if rename_icon:
            rename_action.setIcon(rename_icon)
        rename_action.triggered.connect(self.rename_icon)
        menu.addAction(rename_action)
        
        # Remove action
        remove_action = QAction("Видалити з доку", self)
        remove_icon = get_wdock_icon("remove_app", size=16, is_dark=is_dark)
        if remove_icon:
            remove_action.setIcon(remove_icon)
        remove_action.triggered.connect(self.remove_from_dock)
        menu.addAction(remove_action)
        
        # Properties action
        properties_action = QAction("Властивості ярлика", self)
        properties_icon = get_wdock_icon("settings_main", size=16, is_dark=is_dark)
        if properties_icon:
            properties_action.setIcon(properties_icon)
        properties_action.triggered.connect(self.show_properties)
        menu.addAction(properties_action)
        
        menu.addSeparator()
        
        # Complete dock menu - same as right-clicking on dock
        self.add_complete_dock_menu(menu)
        
        # Show menu
        global_pos = self.mapToGlobal(position)
        menu.exec(global_pos)
    
    def add_complete_dock_menu(self, menu: QMenu):
        """Add complete dock menu actions (same as dock context menu)"""
        # Import here to avoid circular imports
        from ..utils.lucide_icons import get_wdock_icon
        
        # Get dock window to access config manager and theme
        dock_window = self.get_dock_window()
        if not dock_window:
            return
        
        config_manager = dock_window.config_manager
        
        # Detect current theme for proper icon colors
        theme = config_manager.get("theme", "auto")
        if theme == "auto":
            is_dark = dock_window.is_dark_theme()
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
        
        current_pos = config_manager.get("position", "bottom")
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
        
        current_align = config_manager.get("alignment", "center")
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
        auto_hide_value = config_manager.get("auto_hide", True)
        auto_hide_action.setChecked(bool(auto_hide_value) if auto_hide_value is not None else True)
        auto_hide_action.triggered.connect(self.toggle_auto_hide)
        menu.addAction(auto_hide_action)
        
        # Intelligent hide action
        intelligent_hide_action = QAction("Розумне приховування", self)
        intelligent_hide_action.setCheckable(True)
        intelligent_hide_value = config_manager.get("intelligent_hide", True)
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
    
    def rename_icon(self):
        """Rename the icon (change display name)"""
        from PyQt6.QtWidgets import QInputDialog
        
        current_name = self.icon_data.get("name", "")
        new_name, ok = QInputDialog.getText(
            self, "Перейменування", "Нова назва:", text=current_name
        )
        
        if ok and new_name.strip():
            self.icon_data["name"] = new_name.strip()
            self.setToolTip(new_name.strip())
            # TODO: Update in config manager
    
    def remove_from_dock(self):
        """Remove this icon from the dock"""
        from PyQt6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self, "Видалення", 
            f"Видалити '{self.icon_data.get('name', 'цей ярлик')}' з доку?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # TODO: Remove from config and parent layout
            self.setParent(None)
            self.deleteLater()
    
    def show_properties(self):
        """Show Windows properties dialog for the shortcut"""
        try:
            app_path = self.icon_data.get("path", "")
            if app_path and os.path.exists(app_path):
                # Use shell32 to show properties
                import ctypes
                ctypes.windll.shell32.ShellExecuteW(
                    None, "properties", app_path, None, None, 1
                )
        except Exception as e:
            print(f"Error showing properties: {e}")
    
    def change_dock_position(self, position: str):
        """Change dock position"""
        # Get parent dock window and signal position change
        dock_window = self.get_dock_window()
        if dock_window:
            dock_window.change_dock_position(position)
    
    def change_dock_alignment(self, alignment: str):
        """Change dock alignment"""
        # Get parent dock window and signal alignment change
        dock_window = self.get_dock_window()
        if dock_window:
            dock_window.change_dock_alignment(alignment)
    
    def toggle_auto_hide(self):
        """Toggle auto-hide functionality"""
        dock_window = self.get_dock_window()
        if dock_window:
            dock_window.toggle_auto_hide()
    
    def toggle_intelligent_hide(self):
        """Toggle intelligent hide functionality"""
        dock_window = self.get_dock_window()
        if dock_window:
            dock_window.toggle_intelligent_hide()
    
    def show_settings(self):
        """Show settings window"""
        dock_window = self.get_dock_window()
        if dock_window:
            dock_window.show_settings()
    
    def show_about(self):
        """Show about window"""
        dock_window = self.get_dock_window()
        if dock_window:
            dock_window.show_about()
    
    def quit_application(self):
        """Quit the application"""
        dock_window = self.get_dock_window()
        if dock_window:
            dock_window.quit_application()
    
    def get_dock_window(self):
        """Get the parent dock window"""
        # Traverse up the parent hierarchy to find the dock window
        parent = self.parent()
        while parent:
            if hasattr(parent, '__class__') and parent.__class__.__name__ == 'DockWindow':
                return parent
            parent = parent.parent()
        return None