"""
Configuration Manager for WDock
Handles loading, saving, and managing application settings
"""

import os
import json
from typing import Dict, Any, List
from pathlib import Path


class ConfigManager:
    """Manages WDock configuration settings"""
    
    def __init__(self):
        self.config_dir = Path(os.environ.get('APPDATA', '')) / 'WDock'
        self.config_file = self.config_dir / 'config.json'
        self.default_config = {
            "position": "bottom",
            "alignment": "center",
            "auto_hide": True,
            "intelligent_hide": True,
            "always_on_top": True,
            "theme": "auto",  # "dark", "light", "auto"
            "icon_size": 48,
            "animation_speed": 200,  # milliseconds
            "icons": [],
            "groups": {}
        }
        self.config = self.load_config()
    
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
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value and save"""
        self.config[key] = value
        self.save_config()
    
    def add_icon(self, path: str, name: str = None, group: str = None):
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
    
    def add_group(self, name: str, display_name: str = None, icon: str = "📁"):
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
    
    def get_groups(self) -> Dict[str, Any]:
        """Get all groups"""
        return self.config.get("groups", {})