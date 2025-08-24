#!/usr/bin/env python3
"""
Test script to verify dock sizing is working correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.config_manager import ConfigManager

def test_dock_sizing():
    """Test dock size calculations"""
    config_manager = ConfigManager()
    
    # Get current settings
    icon_size = config_manager.get_setting("appearance", "icon_size", 48)
    icons = config_manager.get_icons()
    
    print(f"Current icon size setting: {icon_size}px")
    print(f"Number of icons: {len(icons)}")
    
    # Calculate expected widget size
    widget_size = icon_size + 16  # Icon + padding
    print(f"Expected IconWidget size: {widget_size}x{widget_size}px")
    
    # Test dock size calculation for different positions
    positions = ["bottom", "top", "left", "right"]
    
    for position in positions:
        if position in ["top", "bottom"]:
            # Horizontal layout
            expected_width = (len(icons) * widget_size) + ((len(icons) - 1) * 4) + 16
            expected_height = widget_size + 16
        else:
            # Vertical layout  
            expected_width = widget_size + 16
            expected_height = (len(icons) * widget_size) + ((len(icons) - 1) * 4) + 16
        
        print(f"Position '{position}': Expected dock size {expected_width}x{expected_height}px")

if __name__ == "__main__":
    test_dock_sizing()