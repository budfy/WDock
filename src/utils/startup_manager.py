"""
Startup Manager for WDock
Handles Windows Registry integration for auto-startup functionality
"""

import os
import sys
from pathlib import Path


class StartupManager:
    """Manages Windows startup registry entries for WDock"""
    
    def __init__(self):
        self.app_name = "WDock"
        self.app_path = self.get_app_path()
        self.registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    def get_app_path(self) -> str:
        """Get the full path to the WDock executable"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            return sys.executable
        else:
            # Running as script
            script_path = Path(__file__).parent.parent.parent / "main.py"
            python_exe = sys.executable
            return f'"{python_exe}" "{script_path.absolute()}"'
    
    def is_startup_enabled(self) -> bool:
        """Check if WDock is set to start with Windows"""
        try:
            import winreg
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_key, 0, winreg.KEY_READ) as key:
                try:
                    value, _ = winreg.QueryValueEx(key, self.app_name)
                    return value == self.app_path
                except FileNotFoundError:
                    return False
        except Exception as e:
            print(f"Error checking startup status: {e}")
            return False
    
    def enable_startup(self) -> bool:
        """Enable WDock to start with Windows"""
        try:
            import winreg
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_key, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, self.app_path)
            
            return True
        except Exception as e:
            print(f"Error enabling startup: {e}")
            return False
    
    def disable_startup(self) -> bool:
        """Disable WDock startup with Windows"""
        try:
            import winreg
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_key, 0, winreg.KEY_SET_VALUE) as key:
                try:
                    winreg.DeleteValue(key, self.app_name)
                    return True
                except FileNotFoundError:
                    # Already not in startup
                    return True
        except Exception as e:
            print(f"Error disabling startup: {e}")
            return False
    
    def toggle_startup(self) -> bool:
        """Toggle startup status"""
        if self.is_startup_enabled():
            return self.disable_startup()
        else:
            return self.enable_startup()
    
    def get_startup_status_text(self) -> str:
        """Get human-readable startup status"""
        if self.is_startup_enabled():
            return "WDock запускается при старте Windows"
        else:
            return "WDock не запускается при старте Windows"
    
    def cleanup_registry(self) -> bool:
        """Clean up registry entries (for uninstallation)"""
        try:
            return self.disable_startup()
        except Exception as e:
            print(f"Error cleaning up registry: {e}")
            return False