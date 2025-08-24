"""
Test updated components with Lucide icons
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all updated component imports"""
    try:
        from src.core.system_tray import SystemTrayManager
        print("✓ SystemTrayManager with Lucide icons: OK")
    except Exception as e:
        print(f"✗ SystemTrayManager error: {e}")
    
    try:
        from src.ui.about_window import AboutWindow
        print("✓ AboutWindow with Lucide icons: OK")
    except Exception as e:
        print(f"✗ AboutWindow error: {e}")
    
    try:
        from src.ui.settings_window import SettingsWindow
        print("✓ SettingsWindow with Lucide icons: OK")
    except Exception as e:
        print(f"✗ SettingsWindow error: {e}")
    
    try:
        from src.utils.lucide_icons import get_wdock_icon, get_lucide_icons
        icons = get_lucide_icons()
        print(f"✓ Lucide icons available: {len(icons.ICONS)} icons")
        print(f"✓ WDock mappings available: {len(icons.ICON_MAPPING)} mappings")
    except Exception as e:
        print(f"✗ Lucide icons error: {e}")

if __name__ == "__main__":
    test_imports()