"""
Test script to verify settings window theme functionality in WDock
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.config_manager import ConfigManager
from src.ui.settings_window import SettingsWindow

def test_settings_theme():
    """Test function to verify settings window theme"""
    app = QApplication(sys.argv)
    
    # Initialize configuration manager
    config_manager = ConfigManager()
    
    # Test with different theme settings
    print("Testing settings window theme functionality...")
    
    # Test auto theme (should follow system)
    config_manager.set("theme", "auto")
    settings_window = SettingsWindow(config_manager)
    print(f"Auto theme - Is dark: {settings_window.get_current_theme_is_dark()}")
    settings_window.show()
    
    def test_dark_theme():
        """Test dark theme"""
        print("Switching to dark theme...")
        config_manager.set("theme", "dark")
        settings_window.apply_styles()
        print(f"Dark theme - Is dark: {settings_window.get_current_theme_is_dark()}")
    
    def test_light_theme():
        """Test light theme"""
        print("Switching to light theme...")
        config_manager.set("theme", "light")
        settings_window.apply_styles()
        print(f"Light theme - Is dark: {settings_window.get_current_theme_is_dark()}")
    
    def close_app():
        """Close the application"""
        print("Theme test completed!")
        app.quit()
    
    # Schedule theme changes
    QTimer.singleShot(2000, test_dark_theme)   # Switch to dark after 2 seconds
    QTimer.singleShot(4000, test_light_theme)  # Switch to light after 4 seconds
    QTimer.singleShot(6000, close_app)         # Close after 6 seconds
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_settings_theme()