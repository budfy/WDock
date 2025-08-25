"""
About Window for WDock
Shows application information and version details
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTextEdit, QApplication)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QBrush, QPen
import sys

from ..utils.lucide_icons import get_wdock_icon


class AboutWindow(QDialog):
    """About dialog showing application information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Про програму WDock")
        self.setFixedSize(520, 450)  # Increased height from 400 to 450 pixels
        self.setModal(True)
        
        # Remove question mark button
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)
        
        # Header section with logo and title
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)  # Increased spacing between logo and text
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = self.create_logo()
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setFixedWidth(100)  # Increased width for logo area
        header_layout.addWidget(logo_label)
        
        # Title and version
        title_layout = QVBoxLayout()
        title_layout.setSpacing(8)  # Increased spacing between title elements
        title_layout.setContentsMargins(0, 5, 0, 0)  # Added top margin
        
        # Add more space at the beginning to ensure title is fully visible
        title_layout.addSpacing(5)
        
        title_label = QLabel("WDock")
        title_label.setObjectName("titleLabel")
        title_font = QFont("Segoe UI", 20, QFont.Weight.Bold)  # Further reduced font size
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_layout.addWidget(title_label)
        
        version_label = QLabel("Версія 1.0.0")
        version_label.setObjectName("versionLabel")
        version_font = QFont("Segoe UI", 12)
        version_label.setFont(version_font)
        version_label.setStyleSheet("color: #666666;")
        title_layout.addWidget(version_label)
        
        subtitle_label = QLabel("Сучасна док-панель для Windows")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_font = QFont("Segoe UI", 10)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #888888;")
        title_layout.addWidget(subtitle_label)
        
        title_layout.addStretch()
        header_layout.addLayout(title_layout)
        
        layout.addLayout(header_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Description
        description_text = QTextEdit()
        description_text.setReadOnly(True)
        description_text.setMinimumHeight(180)  # Increased from 140 to 180
        description_text.setMaximumHeight(200)  # Increased from 160 to 200
        description_text.setFrameShape(QFrame.Shape.NoFrame)  # Remove border for cleaner look
        
        # Make the text bolder and more visible with explicit HTML styling
        description_content = """
<div style="color: inherit; font-weight: normal; font-size: 12pt;">
<p><b style="font-weight: bold; color: inherit;">WDock</b> - це сучасна і налаштовувана док-панель для Windows, яка надає швидкий доступ до ваших улюблених застосунків.</p>

<p><b style="font-weight: bold; color: inherit;">Основні можливості:</b></p>
<ul style="margin-top: 5px; margin-left: -20px; color: inherit;">
<li>Адаптивні іконки з ефектами наведення</li>
<li>Групування ярликів перетягуванням</li>
<li>Розумне автоприховування при повноекранних застосунках</li>
<li>Підтримка темної і світлої теми</li>
<li>Плавні анімації і ефекти</li>
<li>Підтримка декількох моніторів</li>
</ul>
</div>
        """
        
        description_text.setHtml(description_content)
        layout.addWidget(description_text)
        
        # System info
        info_layout = QVBoxLayout()
        
        # Python version
        python_version = f"Python {sys.version.split()[0]}"
        python_label = QLabel(f"Побудовано на: {python_version}")
        python_label.setObjectName("pythonLabel")
        python_label.setStyleSheet("font-size: 10px;")
        info_layout.addWidget(python_label)
        
        # PyQt version
        from PyQt6.QtCore import QT_VERSION_STR
        pyqt_version = f"PyQt {QT_VERSION_STR}"
        pyqt_label = QLabel(f"GUI Framework: {pyqt_version}")
        pyqt_label.setObjectName("pyqtLabel")
        pyqt_label.setStyleSheet("font-size: 10px;")
        info_layout.addWidget(pyqt_label)
        
        layout.addLayout(info_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Import here to avoid issues
        from ..utils.lucide_icons import get_wdock_icon
        
        # Detect current theme from parent dock window
        is_dark = self.is_dark_theme()
        
        # GitHub button (placeholder for future)
        github_button = QPushButton("GitHub")
        github_icon = get_wdock_icon("external", size=16, is_dark=is_dark)
        if github_icon:
            github_button.setIcon(github_icon)
        github_button.clicked.connect(self.open_github)
        button_layout.addWidget(github_button)
        
        button_layout.addStretch()
        
        # Close button
        close_button = QPushButton("Закрити")
        close_icon = get_wdock_icon("close", size=16, is_dark=is_dark)
        if close_icon:
            close_button.setIcon(close_icon)
        close_button.clicked.connect(self.accept)
        close_button.setDefault(True)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def is_dark_theme(self) -> bool:
        """Detect if the application should use dark theme"""
        # Try to get theme from parent dock window
        try:
            parent = self.parent()
            # Check if parent is a DockWindow instance
            from ..core.dock_window import DockWindow
            if parent and isinstance(parent, DockWindow):
                theme = parent.config_manager.get("theme", "auto")
                if theme == "auto":
                    # Detect Windows theme automatically
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
                else:
                    return theme == "dark"
            else:
                # Fallback to system detection
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
        except:
            # Fallback to system detection
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
    
    def create_logo(self) -> QPixmap:
        """Create application logo"""
        size = 64
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Main dock base
        dock_rect = QRect(8, 45, 48, 12)
        painter.fillRect(dock_rect, QBrush(QColor(70, 130, 200)))
        
        # Border
        painter.setPen(QPen(QColor(50, 100, 170), 2))
        painter.drawRect(dock_rect)
        
        # App icons on dock
        icon_colors = [
            QColor(255, 100, 100),  # Red
            QColor(100, 255, 100),  # Green
            QColor(100, 100, 255),  # Blue
            QColor(255, 255, 100),  # Yellow
            QColor(255, 100, 255),  # Magenta
        ]
        
        for i, color in enumerate(icon_colors):
            x = 12 + i * 8
            y = 20
            
            # Icon background
            icon_rect = QRect(x, y, 6, 6)
            painter.fillRect(icon_rect, QBrush(color))
            
            # Icon border
            painter.setPen(QPen(color.darker(150), 1))
            painter.drawRect(icon_rect)
            
            # Connection line to dock
            painter.setPen(QPen(QColor(150, 150, 150), 1))
            painter.drawLine(x + 3, y + 6, x + 3, 45)
        
        painter.end()
        return pixmap
    
    def apply_styles(self):
        """Apply custom styles to the dialog based on theme"""
        # Detect current theme
        is_dark = self.is_dark_theme()
        
        if is_dark:
            # Dark theme colors
            bg_color = "#1A1A1A"  # Dark background
            text_color = "#FFFFFF"  # Pure white for all text
            description_bg = "#262626"  # Slightly lighter than background
            description_text = "#FFFFFF"  # Pure white for description text
            border_color = "#555555"
            button_bg = "#3D3D3D"
            button_hover = "#4D4D4D"
            button_pressed = "#5D5D5D"
            button_border = "#666666"
            default_button_bg = "#0078D7"
            default_button_hover = "#0066B5"
            separator_color = "#555555"
        else:
            # Light theme colors
            bg_color = "#FFFFFF"  # Pure white background
            text_color = "#000000"  # Pure black for all text
            description_bg = "#F5F5F5"  # Very light gray
            description_text = "#000000"  # Pure black for description text
            border_color = "#CCCCCC"
            button_bg = "#F0F0F0"
            button_hover = "#E0E0E0"
            button_pressed = "#D0D0D0"
            button_border = "#CCCCCC"
            default_button_bg = "#0078D7"
            default_button_hover = "#0066B5"
            separator_color = "#E0E0E0"
        
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
                color: {text_color};
            }}
            QLabel {{
                color: {text_color};
            }}
            QLabel#titleLabel {{
                color: {text_color};
                font-weight: bold;
                margin-top: 10px;
                font-size: 20pt;
            }}
            QLabel#versionLabel, QLabel#subtitleLabel {{
                color: {text_color};
                margin: 2px 0;
                padding: 0;
                font-weight: medium;
            }}
            QLabel#pythonLabel, QLabel#pyqtLabel {{
                color: {text_color};
                font-size: 10px;
                margin: 2px 0;
                font-weight: medium;
            }}
            QPushButton {{
                background-color: {button_bg};
                border: 1px solid {button_border};
                border-radius: 4px;
                padding: 8px 18px;
                font-size: 11px;
                color: {text_color};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {button_hover};
            }}
            QPushButton:pressed {{
                background-color: {button_pressed};
            }}
            QPushButton:default {{
                background-color: {default_button_bg};
                color: white;
                border-color: #005A9E;
            }}
            QPushButton:default:hover {{
                background-color: {default_button_hover};
            }}
            QTextEdit {{
                background-color: {description_bg};
                color: {description_text};
                font-size: 12px;
                padding: 12px;
                border-radius: 4px;
                margin: 4px 0;
                font-weight: normal;
                line-height: 1.5;
            }}
            QFrame {{
                color: {separator_color};
            }}
        """)
    
    def open_github(self):
        """Open GitHub repository (placeholder)"""
        from PyQt6.QtWidgets import QMessageBox
        
        QMessageBox.information(
            self,
            "GitHub",
            "GitHub repository буде доступний в майбутніх версіях.\n\nСлідкуйте за оновленнями!"
        )