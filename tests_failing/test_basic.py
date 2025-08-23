"""
Basic Test for WDock
Simple test to verify core functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.config_manager import ConfigManager
from src.core.dock_window import DockWindow
from src.core.system_tray import SystemTrayManager

def test_config_manager():
    """Test configuration manager"""
    print("Testing ConfigManager...")
    
    config = ConfigManager()
    
    # Test default values
    assert config.get("position") == "bottom"
    assert config.get("alignment") == "center"
    assert config.get("auto_hide") == True
    
    # Test setting values
    config.set("position", "top")
    assert config.get("position") == "top"
    
    print("✓ ConfigManager tests passed")

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from src.ui.icon_widget import IconWidget
        from src.ui.group_widget import GroupWidget
        from src.ui.about_window import AboutWindow
        from src.utils.drag_drop import DragDropHelper
        print("✓ All modules imported successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    return True

def main():
    """Run basic tests"""
    print("=== WDock Basic Tests ===")
    
    # Test imports
    if not test_imports():
        return
    
    # Test config manager
    test_config_manager()
    
    print("\n=== All Tests Passed! ===")
    print("WDock core functionality is working correctly.")
    print("\nTo run WDock, use: python main.py")

if __name__ == "__main__":
    main()