"""
Test script for Lucide icons integration in WDock
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from src.utils.lucide_icons import get_lucide_icons, get_wdock_icon

def test_lucide_icons():
    """Test Lucide icon integration"""
    app = QApplication(sys.argv)
    
    # Create test window
    window = QMainWindow()
    window.setWindowTitle("WDock Lucide Icons Test")
    window.setGeometry(100, 100, 400, 300)
    
    # Create central widget and layout
    central_widget = QWidget()
    layout = QVBoxLayout()
    
    # Test icon creation
    lucide = get_lucide_icons()
    
    # Test different WDock icons
    test_icons = [
        ("tray_icon", "System Tray Icon"),
        ("settings_main", "Settings Icon"),
        ("about", "About Icon"),
        ("add_app", "Add Application Icon"),
        ("theme_light", "Light Theme Icon"),
        ("theme_dark", "Dark Theme Icon"),
    ]
    
    for icon_name, description in test_icons:
        # Test light theme
        light_icon = get_wdock_icon(icon_name, size=24, is_dark=False)
        # Test dark theme
        dark_icon = get_wdock_icon(icon_name, size=24, is_dark=True)
        
        if light_icon and dark_icon:
            label = QLabel(f"✓ {description} - OK")
            label.setStyleSheet("color: green;")
        else:
            label = QLabel(f"✗ {description} - FAILED")
            label.setStyleSheet("color: red;")
        
        layout.addWidget(label)
    
    # Test available icons list
    available_icons = list(lucide.ICONS.keys())
    mapping_icons = list(lucide.ICON_MAPPING.keys())
    
    layout.addWidget(QLabel(f"\nAvailable Lucide icons: {len(available_icons)}"))
    layout.addWidget(QLabel(f"WDock icon mappings: {len(mapping_icons)}"))
    
    # Summary
    summary_label = QLabel("\nLucide Icons Integration Test Complete!")
    summary_label.setStyleSheet("font-weight: bold; color: blue;")
    layout.addWidget(summary_label)
    
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    
    # Show window
    window.show()
    
    print("Lucide Icons Test Results:")
    print(f"- Available Lucide icons: {len(available_icons)}")
    print(f"- WDock icon mappings: {len(mapping_icons)}")
    print(f"- SVG rendering: {'✓ Working' if light_icon else '✗ Failed'}")
    
    return app.exec()

if __name__ == "__main__":
    test_lucide_icons()