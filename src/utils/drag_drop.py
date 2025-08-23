"""
Drag & Drop Utilities for WDock
Helper functions for enhanced drag and drop functionality
"""

from PyQt6.QtCore import QMimeData, Qt, QPoint
from PyQt6.QtGui import QDrag, QPainter, QPixmap
from PyQt6.QtWidgets import QWidget, QApplication


class DragDropHelper:
    """Helper class for drag and drop operations"""
    
    @staticmethod
    def create_drag_pixmap(widget: QWidget) -> QPixmap:
        """Create a pixmap for dragging from a widget"""
        pixmap = QPixmap(widget.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Make it semi-transparent
        painter.setOpacity(0.7)
        widget.render(painter)
        painter.end()
        
        return pixmap
    
    @staticmethod
    def start_icon_drag(widget: QWidget, icon_data: dict):
        """Start dragging an icon widget"""
        drag = QDrag(widget)
        mime_data = QMimeData()
        
        # Store icon data as JSON
        import json
        mime_data.setText(json.dumps(icon_data))
        mime_data.setData("application/x-wdock-icon", json.dumps(icon_data).encode())
        
        # Create drag pixmap
        drag_pixmap = DragDropHelper.create_drag_pixmap(widget)
        drag.setPixmap(drag_pixmap)
        drag.setHotSpot(QPoint(widget.width() // 2, widget.height() // 2))
        drag.setMimeData(mime_data)
        
        # Execute drag
        result = drag.exec(Qt.DropAction.MoveAction | Qt.DropAction.CopyAction)
        return result
    
    @staticmethod
    def is_wdock_icon_drag(mime_data: QMimeData) -> bool:
        """Check if mime data contains WDock icon data"""
        return mime_data.hasFormat("application/x-wdock-icon")
    
    @staticmethod
    def extract_icon_data(mime_data: QMimeData) -> dict:
        """Extract icon data from mime data"""
        if DragDropHelper.is_wdock_icon_drag(mime_data):
            import json
            data = mime_data.data("application/x-wdock-icon").data().decode()
            return json.loads(data)
        return None
    
    @staticmethod
    def is_external_file_drag(mime_data: QMimeData) -> bool:
        """Check if mime data contains external files"""
        return mime_data.hasUrls()
    
    @staticmethod
    def extract_file_paths(mime_data: QMimeData) -> list:
        """Extract file paths from mime data"""
        paths = []
        if mime_data.hasUrls():
            for url in mime_data.urls():
                path = url.toLocalFile()
                if path.endswith(('.lnk', '.exe', '.url')):
                    paths.append(path)
        return paths


class DropZoneWidget(QWidget):
    """Visual drop zone indicator"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVisible(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
    def show_drop_zone(self, geometry):
        """Show drop zone with specific geometry"""
        self.setGeometry(geometry)
        self.setVisible(True)
        
        # Style the drop zone
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(100, 150, 255, 100);
                border: 2px dashed rgba(100, 150, 255, 200);
                border-radius: 8px;
            }
        """)
    
    def hide_drop_zone(self):
        """Hide the drop zone"""
        self.setVisible(False)


class GroupDropZone(QWidget):
    """Special drop zone for creating groups"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVisible(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
    def show_group_zone(self, geometry):
        """Show group creation zone"""
        self.setGeometry(geometry)
        self.setVisible(True)
        
        # Style for group creation
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 200, 100, 120);
                border: 2px dashed rgba(255, 150, 50, 200);
                border-radius: 12px;
            }
        """)
    
    def hide_group_zone(self):
        """Hide the group zone"""
        self.setVisible(False)