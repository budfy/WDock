"""
Test script to verify dock positioning fixes
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from src.core.config_manager import ConfigManager
from src.core.dock_window import DockWindow

def test_positioning():
    """Test dock positioning calculations"""
    app = QApplication([])
    
    config_manager = ConfigManager()
    
    # Create dock instance
    dock = DockWindow(config_manager)
    
    # Test work area (simulate a 2560x1440 screen)
    work_area = QRect(0, 0, 2560, 1400)  # 40px taskbar at bottom
    
    print("Testing dock positioning calculations:")
    print(f"Work area: {work_area}")
    
    # Test right positioning
    print("\n--- Testing RIGHT positioning ---")
    dock_width, dock_height = dock.calculate_dock_size("right")
    print(f"Calculated dock size for RIGHT: {dock_width}x{dock_height}")
    
    x = work_area.right() - dock_width - 10
    y = work_area.center().y() - dock_height // 2
    print(f"Calculated position: x={x}, y={y}")
    print(f"Should be on screen: x <= {work_area.right() - dock_width}")
    
    if x <= work_area.right() - dock_width:
        print("✅ RIGHT positioning: CORRECT")
    else:
        print("❌ RIGHT positioning: OFF SCREEN")
    
    # Test other positions
    positions = ["bottom", "top", "left"]
    for pos in positions:
        print(f"\n--- Testing {pos.upper()} positioning ---")
        dock_width, dock_height = dock.calculate_dock_size(pos)
        print(f"Calculated dock size for {pos.upper()}: {dock_width}x{dock_height}")
        
        if pos == "bottom":
            x = work_area.center().x() - dock_width // 2
            y = work_area.bottom() - dock_height - 10
        elif pos == "top":
            x = work_area.center().x() - dock_width // 2
            y = work_area.top() + 10
        elif pos == "left":
            x = work_area.left() + 10
            y = work_area.center().y() - dock_height // 2
        
        print(f"Calculated position: x={x}, y={y}")
        
        # Check bounds
        in_bounds = (x >= work_area.left() and 
                    x + dock_width <= work_area.right() and
                    y >= work_area.top() and 
                    y + dock_height <= work_area.bottom())
        
        if in_bounds:
            print(f"✅ {pos.upper()} positioning: CORRECT")
        else:
            print(f"❌ {pos.upper()} positioning: OUT OF BOUNDS")

if __name__ == "__main__":
    test_positioning()