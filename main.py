"""
WDock - Windows Dock Application
Main entry point for the application

Author: WDock Project
Version: 1.0.0
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.dock_window import DockWindow
from src.core.config_manager import ConfigManager
from src.core.system_tray import SystemTrayManager
from src.ui.about_window import AboutWindow
from src.ui.settings_window import SettingsWindow
from src.utils.performance import get_performance_monitor, StartupOptimizer


def main():
    """Main function to start the WDock application"""
    # Start performance monitoring
    perf_monitor = get_performance_monitor()
    perf_monitor.start_startup_timer()
    
    # Run startup optimizations
    StartupOptimizer.run_all_optimizations()
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("WDock")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("WDock Project")
    
    # PyQt6 handles high DPI scaling automatically
    
    # Initialize configuration manager
    config_manager = ConfigManager()
    
    # Create the dock window
    dock_window = DockWindow(config_manager)
    
    # Create system tray with dock window reference
    system_tray = SystemTrayManager(config_manager, dock_window)
    
    # Connect system tray signals
    system_tray.show_dock_requested.connect(dock_window.show)
    system_tray.hide_dock_requested.connect(dock_window.hide)
    system_tray.quit_requested.connect(app.quit)
    
    # Connect About window
    def show_about():
        about_window = AboutWindow(dock_window)
        about_window.exec()
    
    # Connect Settings window
    def show_settings():
        settings_window = SettingsWindow(config_manager, dock_window)
        
        # Connect settings signals
        settings_window.position_changed.connect(dock_window.position_dock)
        settings_window.settings_changed.connect(dock_window.load_icons)
        
        settings_window.exec()
    
    system_tray.about_requested.connect(show_about)
    system_tray.settings_requested.connect(show_settings)
    
    # Show system tray
    system_tray.show()
    
    # Show the dock window
    dock_window.show()
    
    # Finish startup timing
    startup_time = perf_monitor.finish_startup_timer()
    print(f"WDock startup completed in {startup_time:.2f} seconds")
    
    # Setup performance monitoring
    def on_memory_warning(memory_mb):
        print(f"Warning: High memory usage detected: {memory_mb:.1f} MB")
    
    perf_monitor.memory_warning.connect(on_memory_warning)
    
    # Start the application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()