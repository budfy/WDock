#!/usr/bin/env python3
"""
Test script for the unified settings system
"""

import sys
import os
import json
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.settings_manager import SettingsManager
from core.config_manager import ConfigManager

def test_unified_settings():
    """Test the unified settings system"""
    print("Testing unified settings system...")
    
    # Test SettingsManager
    settings_manager = SettingsManager()
    print(f"Settings file location: {settings_manager.get_settings_file_path()}")
    
    # Force creation of settings file
    settings_manager.set("appearance", "theme", "light")
    settings_manager.set("appearance", "theme", "auto")  # Restore default
    
    # Test some settings
    print(f"Default position: {settings_manager.get_position()}")
    print(f"Default theme: {settings_manager.get_theme()}")
    print(f"Default icon size: {settings_manager.get_icon_size()}")
    
    # Test ConfigManager with SettingsManager integration
    config_manager = ConfigManager()
    print(f"Config file location: {config_manager.config_file}")
    
    # Force creation of config file
    config_manager.add_icon("test.exe", "Test App")
    config_manager.remove_icon("test.exe")
    
    # Test backward compatibility methods
    print(f"Position via ConfigManager: {config_manager.get_position()}")
    print(f"Theme via ConfigManager: {config_manager.get_theme()}")
    
    # Test setting a value
    original_theme = config_manager.get_theme()
    print(f"Changing theme from {original_theme} to 'dark'...")
    config_manager.set_theme("dark")
    print(f"New theme: {config_manager.get_theme()}")
    
    # Restore original theme
    config_manager.set_theme(original_theme)
    print(f"Restored theme: {config_manager.get_theme()}")
    
    # Show file contents
    print("\n=== Settings file content (settings.json) ===")
    settings_file = Path(settings_manager.get_settings_file_path())
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            print(json.dumps(json.load(f), indent=2, ensure_ascii=False))
    else:
        print("Settings file not found")
    
    print("\n=== Config file content (config.json) ===")
    config_file = Path(config_manager.config_file)
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            print(json.dumps(json.load(f), indent=2, ensure_ascii=False))
    else:
        print("Config file not found")
    
    print("\n✅ Unified settings system test completed successfully!")

if __name__ == "__main__":
    test_unified_settings()