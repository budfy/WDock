"""
Settings Manager for WDock
Handles user-configurable settings in a unified settings.json file
Separates user preferences from application data (icons, groups)
"""

import os
import json
from typing import Dict, Any, List, Optional, Union
from pathlib import Path


class SettingsManager:
    """Manages unified user settings for WDock"""
    
    def __init__(self):
        self.settings_dir = Path(os.environ.get('APPDATA', '')) / 'WDock'
        self.settings_file = self.settings_dir / 'settings.json'
        
        # Default user settings schema
        self.default_settings = {
            # General settings
            "general": {
                "position": "bottom",  # "top", "bottom", "left", "right"
                "alignment": "center",  # "start", "center", "end"
                "startup_with_windows": False
            },
            
            # Appearance settings
            "appearance": {
                "theme": "auto",  # "auto", "light", "dark"
                "icon_size": 48,  # 32-64 pixels
                "animation_speed": 200  # 100-500 milliseconds
            },
            
            # Behavior settings
            "behavior": {
                "auto_hide": True,
                "intelligent_hide": True,
                "auto_hide_delay": 500,  # milliseconds
                "always_on_top": True
            },
            
            # System tray settings
            "system_tray": {
                "show_tray_icon": True,
                "minimize_to_tray": True
            },
            
            # Hotkeys settings (for future implementation)
            "hotkeys": {
                "toggle_dock": "Win+D"  # Future feature
            },
            
            # Performance settings
            "performance": {
                "memory_limit": 50,  # MB
                "update_interval": 500  # milliseconds
            },
            
            # Debug settings
            "debug": {
                "debug_mode": False,
                "show_widget_borders": False
            }
        }
        
        self.settings = self.load_settings()
    
    def ensure_settings_dir(self):
        """Create settings directory if it doesn't exist"""
        self.settings_dir.mkdir(parents=True, exist_ok=True)
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or create default"""
        self.ensure_settings_dir()
        
        if not self.settings_file.exists():
            # First launch - use defaults and save immediately
            settings = self.default_settings.copy()
            self.save_settings(settings)
            return settings
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Merge with defaults to handle new settings
                merged_settings = self._merge_settings(self.default_settings, settings)
                return merged_settings
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"Error loading settings: {e}. Using defaults.")
            return self.default_settings.copy()
    
    def _merge_settings(self, defaults: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge loaded settings with defaults"""
        merged = defaults.copy()
        
        for key, value in loaded.items():
            if key in merged:
                if isinstance(merged[key], dict) and isinstance(value, dict):
                    merged[key] = self._merge_settings(merged[key], value)
                else:
                    merged[key] = value
            else:
                merged[key] = value
        
        return merged
    
    def save_settings(self, settings: Optional[Dict[str, Any]] = None):
        """Save settings to file"""
        if settings is None:
            settings = self.settings
        
        self.ensure_settings_dir()
        
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            self.settings = settings
        except (PermissionError, OSError) as e:
            print(f"Error saving settings: {e}")
    
    def get(self, section: str, key: str, default=None) -> Any:
        """Get a setting value by section and key"""
        try:
            return self.settings.get(section, {}).get(key, default)
        except (KeyError, AttributeError):
            return default
    
    def set(self, section: str, key: str, value: Any):
        """Set a setting value and save"""
        if section not in self.settings:
            self.settings[section] = {}
        
        self.settings[section][key] = value
        self.save_settings()
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire settings section"""
        return self.settings.get(section, {})
    
    def set_section(self, section: str, values: Dict[str, Any]):
        """Set entire settings section and save"""
        self.settings[section] = values
        self.save_settings()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.default_settings.copy()
        self.save_settings()
    
    def reset_section_to_defaults(self, section: str):
        """Reset specific section to defaults"""
        if section in self.default_settings:
            self.settings[section] = self.default_settings[section].copy()
            self.save_settings()
    
    def export_settings(self, file_path: str) -> bool:
        """Export settings to file"""
        try:
            import shutil
            shutil.copy2(self.settings_file, file_path)
            return True
        except Exception as e:
            print(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """Import settings from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            # Validate and merge imported settings
            merged_settings = self._merge_settings(self.default_settings, imported_settings)
            self.save_settings(merged_settings)
            return True
        except Exception as e:
            print(f"Error importing settings: {e}")
            return False
    
    def migrate_from_config(self, config_data: Dict[str, Any]) -> bool:
        """Migrate settings from old config.json format"""
        try:
            # Map old config keys to new settings structure
            migration_map = {
                "position": ("general", "position"),
                "alignment": ("general", "alignment"),
                "theme": ("appearance", "theme"),
                "icon_size": ("appearance", "icon_size"),
                "animation_speed": ("appearance", "animation_speed"),
                "auto_hide": ("behavior", "auto_hide"),
                "intelligent_hide": ("behavior", "intelligent_hide"),
                "always_on_top": ("behavior", "always_on_top"),
                "auto_hide_delay": ("behavior", "auto_hide_delay"),
                "show_tray": ("system_tray", "show_tray_icon"),
                "minimize_to_tray": ("system_tray", "minimize_to_tray"),
                "memory_limit": ("performance", "memory_limit"),
                "update_interval": ("performance", "update_interval"),
                "debug_mode": ("debug", "debug_mode"),
                "show_borders": ("debug", "show_widget_borders")
            }
            
            # Start with defaults
            migrated_settings = self.default_settings.copy()
            
            # Apply migrated values
            for old_key, (section, new_key) in migration_map.items():
                if old_key in config_data:
                    if section not in migrated_settings:
                        migrated_settings[section] = {}
                    migrated_settings[section][new_key] = config_data[old_key]
            
            # Save migrated settings
            self.save_settings(migrated_settings)
            return True
        except Exception as e:
            print(f"Error migrating settings: {e}")
            return False
    
    def get_settings_file_path(self) -> str:
        """Get the path to the settings file"""
        return str(self.settings_file)
    
    # Convenience methods for commonly used settings
    def get_position(self) -> str:
        return self.get("general", "position", "bottom")
    
    def set_position(self, position: str):
        self.set("general", "position", position)
    
    def get_alignment(self) -> str:
        return self.get("general", "alignment", "center")
    
    def set_alignment(self, alignment: str):
        self.set("general", "alignment", alignment)
    
    def get_theme(self) -> str:
        return self.get("appearance", "theme", "auto")
    
    def set_theme(self, theme: str):
        self.set("appearance", "theme", theme)
    
    def get_icon_size(self) -> int:
        return self.get("appearance", "icon_size", 48)
    
    def set_icon_size(self, size: int):
        self.set("appearance", "icon_size", size)
    
    def get_auto_hide(self) -> bool:
        return self.get("behavior", "auto_hide", True)
    
    def set_auto_hide(self, enabled: bool):
        self.set("behavior", "auto_hide", enabled)
    
    def get_show_tray_icon(self) -> bool:
        return self.get("system_tray", "show_tray_icon", True)
    
    def set_show_tray_icon(self, show: bool):
        self.set("system_tray", "show_tray_icon", show)