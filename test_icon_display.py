#!/usr/bin/env python3
"""
Simple icon loading test
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QFileIconProvider
from PyQt6.QtCore import Qt, QFileInfo
from PyQt6.QtGui import QPixmap

def test_icon_loading():
    """Test if QFileIconProvider works for our files"""
    app = QApplication(sys.argv)
    
    from core.config_manager import ConfigManager
    
    config_manager = ConfigManager()
    icons = config_manager.get_icons()
    
    print(f"Testing icon loading for {len(icons)} files...")
    
    provider = QFileIconProvider()
    
    for i, icon_data in enumerate(icons[:3]):
        file_path = icon_data.get('path', '')
        name = icon_data.get('name', 'Unknown')
        
        print(f"\n--- Testing {i+1}: {name} ---")
        print(f"Path: {file_path}")
        
        if os.path.exists(file_path):
            file_info = QFileInfo(file_path)
            icon = provider.icon(file_info)
            
            if not icon.isNull():
                available_sizes = icon.availableSizes()
                print(f"Available sizes: {available_sizes}")
                
                if available_sizes:
                    largest_size = max(available_sizes, key=lambda s: s.width() * s.height())
                    pixmap = icon.pixmap(largest_size)
                    print(f"✅ Icon extracted! Size: {pixmap.width()}x{pixmap.height()}")
                else:
                    print(f"❌ No icon sizes available")
            else:
                print(f"❌ Icon is null")
        else:
            print(f"❌ File does not exist")
    
    print("\n✅ Icon loading test completed!")

if __name__ == "__main__":
    test_icon_loading()