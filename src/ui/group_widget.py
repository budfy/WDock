"""
Group Widget for WDock
Handles grouped shortcuts with expand/collapse functionality
"""

from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMenu, 
                             QFrame, QGraphicsDropShadowEffect, QScrollArea)
from PyQt6.QtCore import (Qt, QTimer, QPropertyAnimation, QEasingCurve, 
                          QRect, pyqtSignal, QPoint, QSize)
from PyQt6.QtGui import (QPixmap, QPainter, QFont, QColor, QBrush, QPen, 
                         QPainterPath, QAction)

from .icon_widget import IconWidget


class GroupWidget(QWidget):
    """Widget representing a group of application icons"""
    
    # Signals
    clicked = pyqtSignal()
    right_clicked = pyqtSignal()
    
    def __init__(self, group_data: dict, icons: list, parent=None):
        super().__init__(parent)
        self.group_data = group_data
        self.icons = icons
        self.is_expanded = False
        self.icon_size = 48
        
        # UI elements
        self.group_icon_label = None
        self.count_label = None
        self.popup_widget = None
        
        # Animations
        self.hover_animation = None
        self.expand_animation = None
        
        self.setup_ui()
        self.setup_animations()
        self.create_group_icon()
        
        # Enable mouse tracking and context menu
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def setup_ui(self):
        """Setup the user interface"""
        self.setFixedSize(64, 64)  # Same as IconWidget
        
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(0)
        
        # Group icon label
        self.group_icon_label = QLabel()
        self.group_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.group_icon_label.setFixedSize(48, 48)
        layout.addWidget(self.group_icon_label)
        
        # Count badge
        self.count_label = QLabel(str(len(self.icons)))
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_label.setFixedSize(16, 16)
        self.count_label.setStyleSheet("""
            QLabel {
                background-color: #FF4444;
                color: white;
                border-radius: 8px;
                font-size: 8px;
                font-weight: bold;
            }
        """)
        
        # Position count label in top-right corner
        self.count_label.setParent(self)
        self.count_label.move(44, 8)
        
        self.setLayout(layout)
        
        # Set tooltip
        group_name = self.group_data.get("name", "Group")
        self.setToolTip(f"{group_name} ({len(self.icons)} items)")
    
    def setup_animations(self):
        """Setup animations"""
        # Hover animation
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(150)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # Expand animation (for popup)
        self.expand_animation = QPropertyAnimation()
        self.expand_animation.setDuration(200)
        self.expand_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def create_group_icon(self):
        """Create the group icon"""
        group_icon_type = self.group_data.get("icon", "📁")
        
        if group_icon_type.startswith("emoji:") or len(group_icon_type) == 1:
            # Use emoji icon
            self.create_emoji_icon(group_icon_type)
        elif group_icon_type.startswith("file:"):
            # Use custom image file
            self.load_custom_icon(group_icon_type[5:])
        else:
            # Create composite icon from group items
            self.create_composite_icon()
    
    def create_emoji_icon(self, emoji: str):
        """Create an icon using emoji"""
        pixmap = QPixmap(self.icon_size, self.icon_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background circle
        rect = QRect(2, 2, self.icon_size - 4, self.icon_size - 4)
        path = QPainterPath()
        path.addEllipse(rect)
        
        # Fill with gradient background
        painter.fillPath(path, QBrush(QColor(70, 130, 200, 180)))
        
        # Draw border
        painter.setPen(QPen(QColor(50, 100, 170), 2))
        painter.drawPath(path)
        
        # Draw emoji
        font = QFont("Segoe UI Emoji", 24)
        painter.setFont(font)
        painter.setPen(QPen(Qt.GlobalColor.white))
        
        # Clean emoji (remove emoji: prefix if present)
        if emoji.startswith("emoji:"):
            emoji = emoji[6:]
        
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, emoji)
        painter.end()
        
        self.group_icon_label.setPixmap(pixmap)
    
    def load_custom_icon(self, icon_path: str):
        """Load custom icon from file"""
        try:
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.icon_size, self.icon_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.group_icon_label.setPixmap(scaled_pixmap)
            else:
                self.create_composite_icon()
        except:
            self.create_composite_icon()
    
    def create_composite_icon(self):
        """Create a composite icon from the first few icons in the group"""
        pixmap = QPixmap(self.icon_size, self.icon_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        rect = QRect(2, 2, self.icon_size - 4, self.icon_size - 4)
        path = QPainterPath()
        path.addRoundedRect(rect, 8, 8)
        
        painter.fillPath(path, QBrush(QColor(100, 100, 100, 200)))
        painter.setPen(QPen(QColor(80, 80, 80), 2))
        painter.drawPath(path)
        
        # Draw mini icons (up to 4 icons in a 2x2 grid)
        mini_size = 16
        positions = [
            (8, 8),    # top-left
            (24, 8),   # top-right
            (8, 24),   # bottom-left
            (24, 24)   # bottom-right
        ]
        
        for i, icon_data in enumerate(self.icons[:4]):
            if i >= 4:
                break
            
            # Create mini icon widget to get the icon
            mini_icon_widget = IconWidget(icon_data)
            mini_pixmap = mini_icon_widget.icon_label.pixmap()
            
            if mini_pixmap and not mini_pixmap.isNull():
                scaled_mini = mini_pixmap.scaled(
                    mini_size, mini_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                x, y = positions[i]
                painter.drawPixmap(x, y, scaled_mini)
        
        # If more than 4 icons, draw "+N" text
        if len(self.icons) > 4:
            painter.setPen(QPen(Qt.GlobalColor.white))
            font = QFont("Segoe UI", 8, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(QRect(28, 28, 16, 16), 
                           Qt.AlignmentFlag.AlignCenter, 
                           f"+{len(self.icons) - 4}")
        
        painter.end()
        self.group_icon_label.setPixmap(pixmap)
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                if self.is_expanded:
                    self.collapse_group()
                else:
                    self.expand_group()
                # Only emit signal if widget is still valid
                if not self.parent() is None:
                    self.clicked.emit()
            elif event.button() == Qt.MouseButton.RightButton:
                # Only emit signal if widget is still valid
                if not self.parent() is None:
                    self.right_clicked.emit()
        except RuntimeError:
            # Widget has been deleted, ignore the event
            pass
        
        super().mousePressEvent(event)
    
    def expand_group(self):
        """Expand the group to show all icons"""
        if self.is_expanded:
            return
        
        self.is_expanded = True
        self.create_popup()
        self.animate_expand(True)
    
    def collapse_group(self):
        """Collapse the group"""
        if not self.is_expanded:
            return
        
        self.is_expanded = False
        self.animate_expand(False)
    
    def create_popup(self):
        """Create the popup widget showing all group icons"""
        if self.popup_widget:
            self.popup_widget.deleteLater()
        
        self.popup_widget = QFrame(self.parent())
        self.popup_widget.setWindowFlags(Qt.WindowType.Popup)
        self.popup_widget.setFrameStyle(QFrame.Shape.StyledPanel)
        
        # Style the popup
        self.popup_widget.setStyleSheet("""
            QFrame {
                background-color: rgba(40, 40, 40, 240);
                border: 1px solid rgba(80, 80, 80, 150);
                border-radius: 12px;
            }
        """)
        
        # Add shadow effect with reduced blur to avoid coordinate issues
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)   # Further reduced from 8 to prevent positioning issues
        shadow.setXOffset(0)
        shadow.setYOffset(1)      # Reduced from 2
        shadow.setColor(QColor(0, 0, 0, 40))  # Reduced opacity from 60
        self.popup_widget.setGraphicsEffect(shadow)
        
        # Layout for icons
        if len(self.icons) <= 6:
            # Single row
            layout = QHBoxLayout()
        else:
            # Use scroll area for many icons
            scroll_area = QScrollArea()
            scroll_widget = QWidget()
            layout = QHBoxLayout()
            scroll_widget.setLayout(layout)
            scroll_area.setWidget(scroll_widget)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            
            main_layout = QVBoxLayout()
            main_layout.addWidget(scroll_area)
            self.popup_widget.setLayout(main_layout)
        
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # Add icon widgets
        for icon_data in self.icons:
            icon_widget = IconWidget(icon_data)
            layout.addWidget(icon_widget)
        
        if len(self.icons) <= 6:
            self.popup_widget.setLayout(layout)
        
        # Position popup
        self.position_popup()
        
        # Show popup
        self.popup_widget.show()
    
    def position_popup(self):
        """Position the popup relative to the group"""
        if not self.popup_widget:
            return
        
        # Calculate popup size
        icon_count = min(len(self.icons), 6)
        popup_width = icon_count * 68 + 16  # 64px icons + spacing + margins
        popup_height = 80
        
        self.popup_widget.resize(popup_width, popup_height)
        
        # Position above the group (or below if not enough space)
        group_pos = self.mapToGlobal(QPoint(0, 0))
        parent_rect = self.parent().geometry() if self.parent() else QRect(0, 0, 1920, 1080)
        
        popup_x = group_pos.x() - (popup_width - self.width()) // 2
        popup_y = group_pos.y() - popup_height - 10
        
        # Ensure popup stays on screen
        if popup_x < 0:
            popup_x = 0
        elif popup_x + popup_width > parent_rect.width():
            popup_x = parent_rect.width() - popup_width
        
        if popup_y < 0:
            popup_y = group_pos.y() + self.height() + 10
        
        self.popup_widget.move(popup_x, popup_y)
    
    def animate_expand(self, expanding: bool):
        """Animate the expansion/collapse"""
        if not self.popup_widget:
            return
        
        if expanding:
            # Animate popup appearance
            self.popup_widget.setProperty("opacity", 0.0)
            
            # Opacity animation would need a custom property
            # For now, just show/hide
            self.popup_widget.show()
        else:
            # Hide popup
            if self.popup_widget:
                self.popup_widget.hide()
                self.popup_widget.deleteLater()
                self.popup_widget = None
    
    def enterEvent(self, event):
        """Handle mouse enter"""
        self.animate_hover(True)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave"""
        self.animate_hover(False)
        
        # Close popup if mouse leaves and we're expanded
        if self.is_expanded and self.popup_widget:
            # Delay closing to allow moving to popup
            QTimer.singleShot(500, self.check_close_popup)
        
        super().leaveEvent(event)
    
    def check_close_popup(self):
        """Check if popup should be closed"""
        try:
            if self.is_expanded and self.popup_widget:
                # Check if mouse is over popup or group
                if not (self.underMouse() or self.popup_widget.underMouse()):
                    self.collapse_group()
        except RuntimeError:
            # Widget has been deleted, ignore the event
            pass
    
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
    
    def show_context_menu(self, position: QPoint):
        """Show context menu for the group"""
        menu = QMenu(self)
        
        # Expand/Collapse action
        if self.is_expanded:
            expand_action = QAction("Згорнути", self)
        else:
            expand_action = QAction("Розгорнути", self)
        expand_action.triggered.connect(
            self.collapse_group if self.is_expanded else self.expand_group
        )
        menu.addAction(expand_action)
        
        # Rename group action
        rename_action = QAction("Перейменувати групу", self)
        rename_action.triggered.connect(self.rename_group)
        menu.addAction(rename_action)
        
        # Change group icon action
        icon_action = QAction("Задати іконку групи", self)
        icon_action.triggered.connect(self.change_group_icon)
        menu.addAction(icon_action)
        
        menu.addSeparator()
        
        # Ungroup action
        ungroup_action = QAction("Розгрупувати", self)
        ungroup_action.triggered.connect(self.ungroup)
        menu.addAction(ungroup_action)
        
        # Delete group action
        delete_action = QAction("Видалити групу", self)
        delete_action.triggered.connect(self.delete_group)
        menu.addAction(delete_action)
        
        menu.addSeparator()
        
        # Dock menu
        dock_menu = menu.addMenu("Меню доку")
        # TODO: Add dock menu actions
        
        # Show menu
        global_pos = self.mapToGlobal(position)
        menu.exec(global_pos)
    
    def rename_group(self):
        """Rename the group"""
        from PyQt6.QtWidgets import QInputDialog
        
        current_name = self.group_data.get("name", "")
        new_name, ok = QInputDialog.getText(
            self, "Перейменування групи", "Нова назва групи:", text=current_name
        )
        
        if ok and new_name.strip():
            self.group_data["name"] = new_name.strip()
            self.setToolTip(f"{new_name.strip()} ({len(self.icons)} items)")
            # TODO: Update in config manager
    
    def change_group_icon(self):
        """Change group icon"""
        from PyQt6.QtWidgets import QInputDialog
        
        # Simple emoji selection for now
        emojis = ["📁", "🎮", "📊", "🛠️", "🎵", "🌐", "🎯", "📝", "🎨", "⚡"]
        
        current_icon = self.group_data.get("icon", "📁")
        new_icon, ok = QInputDialog.getItem(
            self, "Вибрати іконку", "Виберіть іконку для групи:",
            emojis, emojis.index(current_icon) if current_icon in emojis else 0,
            False
        )
        
        if ok:
            self.group_data["icon"] = new_icon
            self.create_group_icon()
            # TODO: Update in config manager
    
    def ungroup(self):
        """Ungroup the items (break up the group)"""
        from PyQt6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self, "Розгрупування", 
            f"Розгрупувати '{self.group_data.get('name', 'цю групу')}'?\nУсі ярлики залишаться в доку.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Get parent dock window and delegate proper ungrouping
            dock_window = self.get_dock_window()
            if dock_window:
                # Use the dock window's proper ungrouping method
                # This handles config cleanup, layout removal, and reloading ungrouped icons
                dock_window.remove_group_widget(self)
            else:
                # Fallback if dock window not found
                self.setParent(None)
                self.deleteLater()
    
    def delete_group(self):
        """Delete the entire group"""
        from PyQt6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self, "Видалення групи", 
            f"Видалити групу '{self.group_data.get('name', '')}'?\nУсі ярлики в групі будуть видалені з доку.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Get parent dock window and delegate proper group deletion
            dock_window = self.get_dock_window()
            if dock_window:
                # Use the dock window's proper group deletion method
                # This handles config cleanup, icon removal, layout removal, and dock size update
                dock_window.delete_group_widget(self)
            else:
                # Fallback if dock window not found
                self.setParent(None)
                self.deleteLater()
    
    def update_count(self):
        """Update the count badge"""
        self.count_label.setText(str(len(self.icons)))
        self.setToolTip(f"{self.group_data.get('name', 'Group')} ({len(self.icons)} items)")
    
    def get_dock_window(self):
        """Get the parent dock window"""
        # Traverse up the parent hierarchy to find the dock window
        parent = self.parent()
        while parent:
            if hasattr(parent, '__class__') and parent.__class__.__name__ == 'DockWindow':
                return parent
            parent = parent.parent()
        return None