"""
Test script to verify dock alignment behavior in WDock
Tests start/center/end alignment for all dock positions
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.dock_window import DockWindow
from src.core.config_manager import ConfigManager

def test_alignment_behavior():
    """Test function to verify dock alignment behavior"""
    app = QApplication(sys.argv)
    
    # Initialize configuration manager
    config_manager = ConfigManager()
    
    # Create the dock window
    dock_window = DockWindow(config_manager)
    dock_window.show()
    
    test_sequence = [
        # (position, alignment, description)
        ("bottom", "start", "Bottom-Left: Dock should be at left edge of screen"),
        ("bottom", "center", "Bottom-Center: Dock should be centered horizontally"),
        ("bottom", "end", "Bottom-Right: Dock should be at right edge of screen"),
        ("top", "start", "Top-Left: Dock should be at left edge of screen"),
        ("top", "center", "Top-Center: Dock should be centered horizontally"),
        ("top", "end", "Top-Right: Dock should be at right edge of screen"),
        ("left", "start", "Left-Top: Dock should be at top edge of screen"),
        ("left", "center", "Left-Center: Dock should be centered vertically"),
        ("left", "end", "Left-Bottom: Dock should be at bottom edge of screen"),
        ("right", "start", "Right-Top: Dock should be at top edge of screen"),
        ("right", "center", "Right-Center: Dock should be centered vertically"),
        ("right", "end", "Right-Bottom: Dock should be at bottom edge of screen"),
    ]
    
    current_test = 0
    
    def run_next_test():
        nonlocal current_test
        if current_test < len(test_sequence):
            position, alignment, description = test_sequence[current_test]
            print(f"Test {current_test + 1}: {description}")
            
            # Set configuration
            config_manager.set("position", position)
            config_manager.set("alignment", alignment)
            
            # Reposition dock
            dock_window.position_dock()
            
            # Print dock geometry for verification
            geo = dock_window.geometry()
            print(f"  Position: {position}, Alignment: {alignment}")
            print(f"  Dock geometry: x={geo.x()}, y={geo.y()}, w={geo.width()}, h={geo.height()}")
            
            current_test += 1
            
            # Schedule next test
            QTimer.singleShot(1500, run_next_test)
        else:
            print("All alignment tests completed!")
            QTimer.singleShot(1000, app.quit)
    
    # Start testing
    QTimer.singleShot(1000, run_next_test)
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_alignment_behavior()