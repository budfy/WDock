"""
About Window for WDock
Shows application information and version details
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTextEdit, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QBrush, QPen
import sys

from ..utils.lucide_icons import get_wdock_icon


class AboutWindow(QDialog):
    """About dialog showing application information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе WDock")
        self.setFixedSize(450, 350)
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
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = self.create_logo()
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)
        
        # Title and version
        title_layout = QVBoxLayout()
        
        title_label = QLabel("WDock")
        title_font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_layout.addWidget(title_label)
        
        version_label = QLabel("Версия 1.0.0")
        version_font = QFont("Segoe UI", 12)
        version_label.setFont(version_font)
        version_label.setStyleSheet("color: #666666;")
        title_layout.addWidget(version_label)
        
        subtitle_label = QLabel("Современная док-панель для Windows")
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
        separator.setStyleSheet("color: #E0E0E0;")
        layout.addWidget(separator)
        
        # Description
        description_text = QTextEdit()
        description_text.setReadOnly(True)
        description_text.setMaximumHeight(120)
        
        description_content = """
<b>WDock</b> - это современная и настраиваемая док-панель для Windows, которая предоставляет быстрый доступ к вашим любимым приложениям.

<b>Основные возможности:</b>
• Адаптивные иконки с эффектами наведения
• Группировка ярликов перетаскиванием
• Умное автоскрытие при полноэкранных приложениях
• Поддержка темной и светлой темы
• Плавные анимации и эффекты
• Поддержка нескольких мониторов
        """
        
        description_text.setHtml(description_content)
        layout.addWidget(description_text)
        
        # System info
        info_layout = QVBoxLayout()
        
        # Python version
        python_version = f"Python {sys.version.split()[0]}"
        python_label = QLabel(f"Построено на: {python_version}")
        python_label.setStyleSheet("color: #666666; font-size: 10px;")
        info_layout.addWidget(python_label)
        
        # PyQt version
        pyqt_version = f"PyQt {Qt.PYQT_VERSION_STR}"
        pyqt_label = QLabel(f"GUI Framework: {pyqt_version}")
        pyqt_label.setStyleSheet("color: #666666; font-size: 10px;")
        info_layout.addWidget(pyqt_label)
        
        layout.addLayout(info_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # GitHub button (placeholder for future)
        github_button = QPushButton("GitHub")
        github_icon = get_wdock_icon("external", size=16)
        if github_icon:
            github_button.setIcon(github_icon)
        github_button.clicked.connect(self.open_github)
        button_layout.addWidget(github_button)
        
        button_layout.addStretch()
        
        # Close button
        close_button = QPushButton("Закрыть")
        close_icon = get_wdock_icon("close", size=16)
        if close_icon:
            close_button.setIcon(close_icon)
        close_button.clicked.connect(self.accept)
        close_button.setDefault(True)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
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
        """Apply custom styles to the dialog"""
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QPushButton {
                background-color: #F0F0F0;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 11px;
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
            QTextEdit {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                background-color: #FAFAFA;
                font-size: 11px;
                padding: 8px;
            }
        """)
    
    def open_github(self):
        """Open GitHub repository (placeholder)"""
        from PyQt6.QtWidgets import QMessageBox
        
        QMessageBox.information(
            self,
            "GitHub",
            "GitHub repository будет доступен в будущих версиях.\n\nСледите за обновлениями!"
        )


# Import sys for version info
import sys