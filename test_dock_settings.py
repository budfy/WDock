"""
Test script to verify settings window theme when opened from dock context menu
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.dock_window import DockWindow
from src.core.config_manager import ConfigManager

def test_dock_settings():
    """Test function to verify settings window theme from dock"""
    app = QApplication(sys.argv)
    
    # Initialize configuration manager
    config_manager = ConfigManager()
    
    # Create the dock window
    dock_window = DockWindow(config_manager)
    dock_window.show()
    
    def test_settings_from_dock():
        """Test opening settings from dock"""
        print("Testing settings window opened from dock...")
        dock_window.show_settings()
        print("Settings window should now be visible with proper theme")
    
    def close_app():
        """Close the application"""
        print("Dock settings test completed!")
        app.quit()
    
    # Schedule tests
    QTimer.singleShot(1000, test_settings_from_dock)  # Open settings after 1 second
    QTimer.singleShot(5000, close_app)                # Close after 5 seconds
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_dock_settings()