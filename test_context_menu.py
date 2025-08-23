"""
Test script to verify context menu functionality in WDock
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QPoint
from PyQt6.QtGui import QMouseEvent

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.dock_window import DockWindow
from src.core.config_manager import ConfigManager

def test_context_menus():
    """Test function to verify context menu functionality"""
    app = QApplication(sys.argv)
    
    # Initialize configuration manager
    config_manager = ConfigManager()
    
    # Create the dock window
    dock_window = DockWindow(config_manager)
    dock_window.show()
    
    def test_dock_context_menu():
        """Test dock context menu"""
        print("Testing dock context menu...")
        # Simulate right-click on dock window
        position = QPoint(50, 25)  # Center of dock
        dock_window.show_dock_context_menu(position)
        print("Dock context menu should now be visible")
    
    def test_icon_context_menu():
        """Test icon context menu if icons exist"""
        print("Testing icon context menu...")
        if hasattr(dock_window, 'dock_layout') and dock_window.dock_layout.count() > 0:
            # Get first icon widget
            icon_widget = dock_window.dock_layout.itemAt(0).widget()
            if hasattr(icon_widget, 'show_context_menu'):
                position = QPoint(24, 24)  # Center of icon
                icon_widget.show_context_menu(position)
                print("Icon context menu should now be visible")
        else:
            print("No icons found to test")
    
    # Schedule tests
    QTimer.singleShot(1000, test_dock_context_menu)  # Test after 1 second
    QTimer.singleShot(3000, test_icon_context_menu)  # Test after 3 seconds
    QTimer.singleShot(5000, app.quit)  # Quit after 5 seconds
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_context_menus()