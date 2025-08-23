"""
Configuration Manager for WDock
Handles loading, saving, and managing application settings
"""

import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

from .settings_manager import SettingsManager


class ConfigManager:
    """Manages WDock application data (icons, groups)
    
    Note: User settings are now handled by SettingsManager.
    This class focuses on application data that's not user-configurable settings.
    """
    
    def __init__(self):
        self.config_dir = Path(os.environ.get('APPDATA', '')) / 'WDock'
        self.config_file = self.config_dir / 'config.json'
        
        # Initialize settings manager for user preferences
        self.settings_manager = SettingsManager()
        
        # Default application data (icons and groups only)
        self.default_config = {
            "icons": [],
            "groups": {}
        }
        
        self.config = self.load_config()
        
        # Perform migration if needed
        self._migrate_user_settings_if_needed()
    
    def ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        self.ensure_config_dir()
        
        is_first_launch = not self.config_file.exists()
        
        if is_first_launch:
            # First launch - use defaults and save immediately
            config = self.default_config.copy()
            # Save the default configuration on first launch
            # This ensures the user sees their choices persisted
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
            except (PermissionError, OSError) as e:
                print(f"Warning: Could not save initial config: {e}")
            return config
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults to handle new settings
                merged_config = self.default_config.copy()
                merged_config.update(config)
                return merged_config
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"Error loading config: {e}. Using defaults.")
            return self.default_config.copy()
    
    def save_config(self):
        """Save current configuration to file"""
        self.ensure_config_dir()
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except (PermissionError, OSError) as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value - delegates user settings to SettingsManager"""
        # Check if this is a user setting that should be delegated
        user_settings_map = {
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
        
        if key in user_settings_map:
            section, setting_key = user_settings_map[key]
            return self.settings_manager.get(section, setting_key, default)
        else:
            # Handle application data (icons, groups)
            return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value - delegates user settings to SettingsManager"""
        # Check if this is a user setting that should be delegated
        user_settings_map = {
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
        
        if key in user_settings_map:
            section, setting_key = user_settings_map[key]
            self.settings_manager.set(section, setting_key, value)
        else:
            # Handle application data (icons, groups)
            self.config[key] = value
            self.save_config()
    
    def add_icon(self, path: str, name: Optional[str] = None, group: Optional[str] = None):
        """Add an icon to the dock"""
        if not name:
            name = Path(path).stem
        
        icon_entry = {
            "path": path,
            "name": name,
            "group": group
        }
        
        self.config["icons"].append(icon_entry)
        self.save_config()
    
    def remove_icon(self, path: str):
        """Remove an icon from the dock"""
        self.config["icons"] = [
            icon for icon in self.config["icons"] 
            if icon["path"] != path
        ]
        self.save_config()
    
    def get_icons(self) -> List[Dict[str, Any]]:
        """Get all icons"""
        return self.config.get("icons", [])
    
    def add_group(self, name: str, display_name: Optional[str] = None, icon: str = "📁"):
        """Add a new group"""
        if not display_name:
            display_name = name
        
        self.config["groups"][name] = {
            "name": display_name,
            "icon": icon,
            "items": []
        }
        self.save_config()
    
    def remove_group(self, name: str):
        """Remove a group and ungroup its items"""
        if name in self.config["groups"]:
            # Remove group reference from icons
            for icon in self.config["icons"]:
                if icon.get("group") == name:
                    icon["group"] = None
            
            # Remove the group
            del self.config["groups"][name]
            self.save_config()
    
    def _migrate_user_settings_if_needed(self):
        """Migrate user settings from config.json to settings.json if needed"""
        # Check if we have old-style settings in config.json
        old_settings_keys = {
            "position", "alignment", "auto_hide", "intelligent_hide", "always_on_top",
            "theme", "icon_size", "animation_speed", "auto_hide_delay", "show_tray",
            "minimize_to_tray", "memory_limit", "update_interval", "debug_mode", "show_borders"
        }
        
        # Check if any old settings exist in current config
        has_old_settings = any(key in self.config for key in old_settings_keys)
        
        if has_old_settings:
            print("Migrating user settings from config.json to settings.json...")
            
            # Migrate to new settings system
            if self.settings_manager.migrate_from_config(self.config):
                # Remove migrated settings from config.json, keep only icons and groups
                new_config = {
                    "icons": self.config.get("icons", []),
                    "groups": self.config.get("groups", {})
                }
                self.config = new_config
                self.save_config()
                print("Migration completed successfully.")
            else:
                print("Migration failed, keeping current configuration.")
    
    # Delegation methods for backward compatibility
    # These methods delegate to SettingsManager for user settings
    
    def get_setting(self, section: str, key: str, default=None):
        """Get a user setting (delegates to SettingsManager)"""
        return self.settings_manager.get(section, key, default)
    
    def set_setting(self, section: str, key: str, value: Any):
        """Set a user setting (delegates to SettingsManager)"""
        self.settings_manager.set(section, key, value)
    
    # Convenience methods for commonly used settings
    def get_position(self) -> str:
        return self.settings_manager.get_position()
    
    def set_position(self, position: str):
        self.settings_manager.set_position(position)
    
    def get_alignment(self) -> str:
        return self.settings_manager.get_alignment()
    
    def set_alignment(self, alignment: str):
        self.settings_manager.set_alignment(alignment)
    
    def get_theme(self) -> str:
        return self.settings_manager.get_theme()
    
    def set_theme(self, theme: str):
        self.settings_manager.set_theme(theme)
    
    def get_icon_size(self) -> int:
        return self.settings_manager.get_icon_size()
    
    def set_icon_size(self, size: int):
        self.settings_manager.set_icon_size(size)
    
    def get_auto_hide(self) -> bool:
        return self.settings_manager.get_auto_hide()
    
    def set_auto_hide(self, enabled: bool):
        self.settings_manager.set_auto_hide(enabled)
    
    def get_groups(self) -> Dict[str, Any]:
        """Get all groups"""
        return self.config.get("groups", {})