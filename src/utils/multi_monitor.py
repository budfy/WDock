"""
Multi-Monitor Support for WDock
Handles multiple monitors and DPI scaling
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QScreen
import ctypes
from ctypes import wintypes
from typing import List, Dict, Tuple, Optional


class MonitorInfo:
    """Information about a single monitor"""
    
    def __init__(self, screen: QScreen, index: int):
        self.screen = screen
        self.index = index
        self.name = screen.name()
        self.geometry = screen.geometry()
        self.available_geometry = screen.availableGeometry()
        self.dpi = screen.logicalDotsPerInch()
        self.device_pixel_ratio = screen.devicePixelRatio()
        self.is_primary = screen == QApplication.primaryScreen()
        
        # Get Windows-specific info
        self.refresh_rate = screen.refreshRate()
        self.depth = screen.depth()
    
    def __str__(self):
        return f"Monitor {self.index}: {self.name} ({self.geometry.width()}x{self.geometry.height()}) DPI:{self.dpi:.0f}"


class MultiMonitorManager:
    """Manages multi-monitor setup and DPI scaling"""
    
    def __init__(self):
        self.monitors: List[MonitorInfo] = []
        self.primary_monitor: Optional[MonitorInfo] = None
        self.current_monitor: Optional[MonitorInfo] = None
        
        self.refresh_monitors()
        
        # Connect to screen changes
        app = QApplication.instance()
        if app:
            app.screenAdded.connect(self.on_screen_added)
            app.screenRemoved.connect(self.on_screen_removed)
    
    def refresh_monitors(self):
        """Refresh the list of available monitors"""
        self.monitors.clear()
        
        app = QApplication.instance()
        if not app:
            return
        
        screens = app.screens()
        primary_screen = app.primaryScreen()
        
        for i, screen in enumerate(screens):
            monitor = MonitorInfo(screen, i)
            self.monitors.append(monitor)
            
            if screen == primary_screen:
                self.primary_monitor = monitor
        
        print(f"Detected {len(self.monitors)} monitors")
        for monitor in self.monitors:
            print(f"  {monitor}")
    
    def get_monitor_at_point(self, x: int, y: int) -> Optional[MonitorInfo]:
        """Get the monitor containing the specified point"""
        for monitor in self.monitors:
            if monitor.geometry.contains(x, y):
                return monitor
        return self.primary_monitor
    
    def get_monitor_for_window(self, window_rect: QRect) -> Optional[MonitorInfo]:
        """Get the monitor that contains most of the window"""
        max_overlap = 0
        best_monitor = None
        
        for monitor in self.monitors:
            overlap_rect = window_rect.intersected(monitor.geometry)
            overlap_area = overlap_rect.width() * overlap_rect.height()
            
            if overlap_area > max_overlap:
                max_overlap = overlap_area
                best_monitor = monitor
        
        return best_monitor or self.primary_monitor
    
    def get_work_area(self, monitor: MonitorInfo = None) -> QRect:
        """Get work area for specific monitor or current monitor"""
        if monitor is None:
            monitor = self.current_monitor or self.primary_monitor
        
        if monitor:
            return monitor.available_geometry
        
        # Fallback to primary screen
        app = QApplication.instance()
        if app:
            return app.primaryScreen().availableGeometry()
        
        return QRect(0, 0, 1920, 1080)  # Ultimate fallback
    
    def get_dpi_scale_factor(self, monitor: MonitorInfo = None) -> float:
        """Get DPI scale factor for monitor"""
        if monitor is None:
            monitor = self.current_monitor or self.primary_monitor
        
        if monitor:
            # Standard DPI is 96
            return monitor.dpi / 96.0
        
        return 1.0
    
    def scale_size_for_dpi(self, size: int, monitor: MonitorInfo = None) -> int:
        """Scale a size value for DPI"""
        scale_factor = self.get_dpi_scale_factor(monitor)
        return int(size * scale_factor)
    
    def get_monitor_list(self) -> List[Dict]:
        """Get list of monitor information for UI display"""
        monitor_list = []
        
        for monitor in self.monitors:
            monitor_dict = {
                "index": monitor.index,
                "name": monitor.name,
                "resolution": f"{monitor.geometry.width()}x{monitor.geometry.height()}",
                "dpi": f"{monitor.dpi:.0f}",
                "scale_factor": f"{self.get_dpi_scale_factor(monitor):.0%}",
                "is_primary": monitor.is_primary,
                "refresh_rate": f"{monitor.refresh_rate:.0f} Hz",
                "position": f"({monitor.geometry.x()}, {monitor.geometry.y()})"
            }
            monitor_list.append(monitor_dict)
        
        return monitor_list
    
    def position_window_on_monitor(self, window_geometry: QRect, monitor_index: int = None) -> QRect:
        """Position a window on a specific monitor"""
        if monitor_index is None or monitor_index >= len(self.monitors):
            monitor = self.primary_monitor
        else:
            monitor = self.monitors[monitor_index]
        
        if not monitor:
            return window_geometry
        
        # Get work area for the monitor
        work_area = monitor.available_geometry
        
        # Calculate centered position
        x = work_area.x() + (work_area.width() - window_geometry.width()) // 2
        y = work_area.y() + (work_area.height() - window_geometry.height()) // 2
        
        # Ensure window fits within work area
        if x + window_geometry.width() > work_area.right():
            x = work_area.right() - window_geometry.width()
        if y + window_geometry.height() > work_area.bottom():
            y = work_area.bottom() - window_geometry.height()
        if x < work_area.x():
            x = work_area.x()
        if y < work_area.y():
            y = work_area.y()
        
        return QRect(x, y, window_geometry.width(), window_geometry.height())
    
    def get_best_monitor_for_dock(self, position: str) -> MonitorInfo:
        """Get the best monitor for dock placement based on position"""
        # For now, use primary monitor
        # In the future, could be configurable or based on cursor position
        return self.primary_monitor or self.monitors[0] if self.monitors else None
    
    def on_screen_added(self, screen: QScreen):
        """Handle screen addition"""
        print(f"Screen added: {screen.name()}")
        self.refresh_monitors()
    
    def on_screen_removed(self, screen: QScreen):
        """Handle screen removal"""
        print(f"Screen removed: {screen.name()}")
        self.refresh_monitors()
    
    def set_current_monitor(self, monitor: MonitorInfo):
        """Set the current monitor for the dock"""
        self.current_monitor = monitor
        print(f"Current monitor set to: {monitor}")
    
    def auto_detect_monitor(self, window_geometry: QRect):
        """Auto-detect and set current monitor based on window position"""
        monitor = self.get_monitor_for_window(window_geometry)
        if monitor:
            self.set_current_monitor(monitor)


class DPIAwareWidget:
    """Mixin class for DPI-aware widgets"""
    
    def __init__(self, monitor_manager: MultiMonitorManager):
        self.monitor_manager = monitor_manager
    
    def scale_for_dpi(self, value: int) -> int:
        """Scale a value for current DPI"""
        return self.monitor_manager.scale_size_for_dpi(value)
    
    def get_scaled_icon_size(self, base_size: int = 48) -> int:
        """Get icon size scaled for current DPI"""
        return self.scale_for_dpi(base_size)
    
    def get_scaled_margin(self, base_margin: int = 8) -> int:
        """Get margin scaled for current DPI"""
        return self.scale_for_dpi(base_margin)
    
    def update_for_dpi_change(self):
        """Update widget when DPI changes"""
        # Override in subclasses to handle DPI changes
        pass


def get_system_dpi_info() -> Dict:
    """Get system-wide DPI information"""
    try:
        # Get system DPI using Windows API
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        
        # Get DPI for primary monitor
        hdc = user32.GetDC(0)
        dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
        dpi_y = ctypes.windll.gdi32.GetDeviceCaps(hdc, 90)  # LOGPIXELSY
        user32.ReleaseDC(0, hdc)
        
        return {
            "dpi_x": dpi_x,
            "dpi_y": dpi_y,
            "scale_factor": dpi_x / 96.0,
            "scale_percent": f"{(dpi_x / 96.0) * 100:.0f}%"
        }
    except Exception as e:
        print(f"Error getting system DPI info: {e}")
        return {"dpi_x": 96, "dpi_y": 96, "scale_factor": 1.0, "scale_percent": "100%"}


# Global monitor manager instance
monitor_manager = None

def get_monitor_manager() -> MultiMonitorManager:
    """Get global monitor manager instance"""
    global monitor_manager
    if monitor_manager is None:
        monitor_manager = MultiMonitorManager()
    return monitor_manager