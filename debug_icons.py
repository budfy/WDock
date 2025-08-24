#!/usr/bin/env python3
"""
Debug script to test icon extraction functionality
"""

import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap
import win32gui
import win32api

def test_icon_extraction():
    """Test icon extraction for common file types"""
    
    app = QApplication(sys.argv)
    
    # Get some sample files from the config
    from core.config_manager import ConfigManager
    config_manager = ConfigManager()
    icons = config_manager.get_icons()
    
    print("Testing icon extraction for dock icons:")
    print(f"Found {len(icons)} icons in configuration")
    
    for i, icon_data in enumerate(icons[:3]):  # Test first 3 icons
        icon_path = icon_data.get("path", "")
        icon_name = icon_data.get("name", "Unknown")
        
        print(f"\n--- Testing icon {i+1}: {icon_name} ---")
        print(f"Path: {icon_path}")
        print(f"File exists: {os.path.exists(icon_path)}")
        
        if not os.path.exists(icon_path):
            print("❌ File does not exist!")
            continue
        
        try:
            if icon_path.endswith('.lnk'):
                print("Testing shortcut icon extraction...")
                pixmap = extract_shortcut_icon_debug(icon_path)
            elif icon_path.endswith('.exe'):
                print("Testing executable icon extraction...")
                pixmap = extract_exe_icon_debug(icon_path)
            else:
                print("Testing image file loading...")
                pixmap = QPixmap(icon_path)
            
            if pixmap and not pixmap.isNull():
                print(f"✅ Icon extracted successfully! Size: {pixmap.width()}x{pixmap.height()}")
            else:
                print("❌ Failed to extract icon - pixmap is null")
                
        except Exception as e:
            print(f"❌ Exception during extraction: {e}")
            import traceback
            traceback.print_exc()

def extract_shortcut_icon_debug(lnk_path: str) -> QPixmap:
    """Debug version of shortcut icon extraction"""
    # Method 1: Try QFileIconProvider first
    try:
        print(f"  Testing QFileIconProvider...")
        from PyQt6.QtWidgets import QFileIconProvider
        from PyQt6.QtCore import QFileInfo
        
        provider = QFileIconProvider()
        file_info = QFileInfo(lnk_path)
        icon = provider.icon(file_info)
        
        if not icon.isNull():
            available_sizes = icon.availableSizes()
            print(f"  Available icon sizes: {available_sizes}")
            if available_sizes:
                largest_size = max(available_sizes, key=lambda s: s.width() * s.height())
                pixmap = icon.pixmap(largest_size)
                
                if not pixmap.isNull() and pixmap.width() > 16:
                    print(f"  ✅ QFileIconProvider succeeded! Size: {pixmap.width()}x{pixmap.height()}")
                    return pixmap
                else:
                    print(f"  QFileIconProvider returned small/generic icon: {pixmap.width()}x{pixmap.height()}")
        else:
            print(f"  QFileIconProvider returned null icon")
    except Exception as e:
        print(f"  QFileIconProvider failed: {e}")
    
    # Method 2: Extract target path and get icon from target
    try:
        print(f"  Testing COM Shell Link method...")
        import pythoncom
        from win32com.shell import shell, shellcon
        
        shortcut = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink
        )
        
        shortcut.QueryInterface(pythoncom.IID_IPersistFile).Load(lnk_path)
        
        target_path, _ = shortcut.GetPath(shell.SLGP_SHORTPATH)
        print(f"  Target path: {target_path}")
        
        if target_path and os.path.exists(target_path):
            return extract_exe_icon_debug(target_path)
        else:
            print(f"  Target path is invalid or doesn't exist")
            
    except Exception as e:
        print(f"  COM Shell Link method failed: {e}")
    
    return None

def extract_exe_icon_debug(exe_path: str) -> QPixmap:
    """Debug version of executable icon extraction"""
    # Method 1: Try QFileIconProvider
    try:
        print(f"  Testing QFileIconProvider for exe...")
        from PyQt6.QtWidgets import QFileIconProvider
        from PyQt6.QtCore import QFileInfo
        
        provider = QFileIconProvider()
        file_info = QFileInfo(exe_path)
        icon = provider.icon(file_info)
        
        if not icon.isNull():
            available_sizes = icon.availableSizes()
            print(f"  Available icon sizes: {available_sizes}")
            if available_sizes:
                largest_size = max(available_sizes, key=lambda s: s.width() * s.height())
                pixmap = icon.pixmap(largest_size)
                
                if not pixmap.isNull():
                    print(f"  ✅ QFileIconProvider succeeded! Size: {pixmap.width()}x{pixmap.height()}")
                    return pixmap
        print(f"  QFileIconProvider returned null or empty icon")
    except Exception as e:
        print(f"  QFileIconProvider failed: {e}")
    
    # Method 2: Try Windows API
    try:
        print(f"  Testing Windows API extraction...")
        large_icons, small_icons = win32gui.ExtractIconEx(exe_path, 0)
        print(f"  Found {len(large_icons)} large icons, {len(small_icons)} small icons")
        
        if large_icons:
            print(f"  ✅ Windows API extraction succeeded (but conversion may fail)")
            
            # Clean up handles
            for icon_handle in large_icons:
                win32gui.DestroyIcon(icon_handle)
            for icon_handle in small_icons:
                win32gui.DestroyIcon(icon_handle)
                
            return True  # Indicate success for debugging
    except Exception as e:
        print(f"  Windows API extraction failed: {e}")
    
    return None

if __name__ == "__main__":
    test_icon_extraction()