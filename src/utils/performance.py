"""
Performance Optimization for WDock
Memory usage optimization and startup performance improvements
"""

import gc
import sys
import psutil
import os
from typing import Dict, Any
from PyQt6.QtCore import QTimer, QObject, pyqtSignal


class PerformanceMonitor(QObject):
    """Monitor and optimize WDock performance"""
    
    # Signals
    memory_warning = pyqtSignal(float)  # Emit when memory usage is high
    performance_stats = pyqtSignal(dict)  # Emit performance statistics
    
    def __init__(self, memory_limit_mb: int = 50):
        super().__init__()
        self.memory_limit_mb = memory_limit_mb
        self.process = psutil.Process(os.getpid())
        self.startup_time = None
        self.icon_cache = {}  # Cache for loaded icons
        self.max_cache_size = 100  # Maximum cached icons
        
        # Performance monitoring timer
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.check_performance)
        self.monitor_timer.start(5000)  # Check every 5 seconds
        
        # Garbage collection timer
        self.gc_timer = QTimer()
        self.gc_timer.timeout.connect(self.optimize_memory)
        self.gc_timer.start(30000)  # Run GC every 30 seconds
    
    def start_startup_timer(self):
        """Start measuring startup time"""
        import time
        self.startup_time = time.time()
    
    def finish_startup_timer(self) -> float:
        """Finish measuring startup time and return duration"""
        if self.startup_time:
            import time
            duration = time.time() - self.startup_time
            self.startup_time = None
            return duration
        return 0.0
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage statistics"""
        try:
            memory_info = self.process.memory_info()
            memory_percent = self.process.memory_percent()
            
            return {
                "rss_mb": memory_info.rss / 1024 / 1024,  # Resident Set Size
                "vms_mb": memory_info.vms / 1024 / 1024,  # Virtual Memory Size
                "percent": memory_percent,
                "limit_mb": self.memory_limit_mb
            }
        except Exception as e:
            print(f"Error getting memory usage: {e}")
            return {"rss_mb": 0, "vms_mb": 0, "percent": 0, "limit_mb": self.memory_limit_mb}
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        memory_stats = self.get_memory_usage()
        
        try:
            cpu_percent = self.process.cpu_percent()
            num_threads = self.process.num_threads()
            num_handles = getattr(self.process, 'num_handles', lambda: 0)()
            
            return {
                "memory": memory_stats,
                "cpu_percent": cpu_percent,
                "num_threads": num_threads,
                "num_handles": num_handles,
                "icon_cache_size": len(self.icon_cache),
                "gc_collections": gc.get_count()
            }
        except Exception as e:
            print(f"Error getting performance stats: {e}")
            return {"memory": memory_stats}
    
    def check_performance(self):
        """Check current performance and emit warnings if needed"""
        stats = self.get_performance_stats()
        self.performance_stats.emit(stats)
        
        # Check memory usage
        memory_mb = stats["memory"]["rss_mb"]
        if memory_mb > self.memory_limit_mb:
            self.memory_warning.emit(memory_mb)
            self.optimize_memory()
    
    def optimize_memory(self):
        """Optimize memory usage"""
        # Force garbage collection
        collected = gc.collect()
        
        # Clean icon cache if too large
        if len(self.icon_cache) > self.max_cache_size:
            # Remove oldest entries (simple LRU)
            items_to_remove = len(self.icon_cache) - self.max_cache_size + 10
            for _ in range(items_to_remove):
                if self.icon_cache:
                    oldest_key = next(iter(self.icon_cache))
                    del self.icon_cache[oldest_key]
        
        print(f"Memory optimization: collected {collected} objects, cache size: {len(self.icon_cache)}")
    
    def cache_icon(self, path: str, pixmap):
        """Cache an icon pixmap for reuse"""
        if len(self.icon_cache) >= self.max_cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self.icon_cache))
            del self.icon_cache[oldest_key]
        
        self.icon_cache[path] = pixmap
    
    def get_cached_icon(self, path: str):
        """Get cached icon pixmap"""
        return self.icon_cache.get(path)
    
    def clear_cache(self):
        """Clear all cached icons"""
        self.icon_cache.clear()
        self.optimize_memory()
    
    def set_memory_limit(self, limit_mb: int):
        """Set memory usage limit"""
        self.memory_limit_mb = limit_mb
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information for optimization"""
        try:
            memory = psutil.virtual_memory()
            cpu_count = psutil.cpu_count()
            
            return {
                "total_memory_gb": memory.total / 1024 / 1024 / 1024,
                "available_memory_gb": memory.available / 1024 / 1024 / 1024,
                "memory_usage_percent": memory.percent,
                "cpu_count": cpu_count,
                "python_version": sys.version,
                "platform": sys.platform
            }
        except Exception as e:
            print(f"Error getting system info: {e}")
            return {}


class StartupOptimizer:
    """Optimize application startup performance"""
    
    @staticmethod
    def optimize_imports():
        """Optimize module imports for faster startup"""
        # Pre-import commonly used modules
        import json
        import os
        import sys
        from pathlib import Path
        
        # Pre-compile regex patterns if needed
        # (Add any frequently used regex patterns here)
        
        print("Import optimization completed")
    
    @staticmethod
    def optimize_ui_loading():
        """Optimize UI component loading"""
        # Pre-load common styles
        # Pre-initialize font metrics
        from PyQt6.QtGui import QFontMetrics, QFont
        font = QFont("Segoe UI", 10)
        QFontMetrics(font)
        
        print("UI optimization completed")
    
    @staticmethod
    def optimize_config_loading():
        """Optimize configuration loading"""
        # Pre-create config directory if needed
        import os
        config_dir = os.path.join(os.environ.get('APPDATA', ''), 'WDock')
        os.makedirs(config_dir, exist_ok=True)
        
        print("Config optimization completed")
    
    @staticmethod
    def run_all_optimizations():
        """Run all startup optimizations"""
        StartupOptimizer.optimize_imports()
        StartupOptimizer.optimize_ui_loading()
        StartupOptimizer.optimize_config_loading()
        
        print("All startup optimizations completed")


class MemoryProfiler:
    """Profile memory usage for debugging"""
    
    def __init__(self):
        self.snapshots = []
    
    def take_snapshot(self, label: str = ""):
        """Take a memory usage snapshot"""
        try:
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            snapshot = {
                "label": label,
                "timestamp": __import__("time").time(),
                "rss_mb": memory_info.rss / 1024 / 1024,
                "vms_mb": memory_info.vms / 1024 / 1024,
                "percent": process.memory_percent()
            }
            
            self.snapshots.append(snapshot)
            return snapshot
        except Exception as e:
            print(f"Error taking memory snapshot: {e}")
            return None
    
    def get_memory_growth(self) -> Dict[str, float]:
        """Calculate memory growth between snapshots"""
        if len(self.snapshots) < 2:
            return {"growth_mb": 0, "growth_percent": 0}
        
        first = self.snapshots[0]
        last = self.snapshots[-1]
        
        growth_mb = last["rss_mb"] - first["rss_mb"]
        growth_percent = ((last["rss_mb"] / first["rss_mb"]) - 1) * 100 if first["rss_mb"] > 0 else 0
        
        return {
            "growth_mb": growth_mb,
            "growth_percent": growth_percent,
            "duration_seconds": last["timestamp"] - first["timestamp"],
            "snapshots_count": len(self.snapshots)
        }
    
    def print_report(self):
        """Print memory profiling report"""
        if not self.snapshots:
            print("No memory snapshots available")
            return
        
        print("\n=== Memory Profiling Report ===")
        for i, snapshot in enumerate(self.snapshots):
            print(f"{i+1}. {snapshot['label']}: {snapshot['rss_mb']:.1f} MB ({snapshot['percent']:.1f}%)")
        
        if len(self.snapshots) >= 2:
            growth = self.get_memory_growth()
            print(f"\nMemory Growth: {growth['growth_mb']:.1f} MB ({growth['growth_percent']:.1f}%)")
            print(f"Duration: {growth['duration_seconds']:.1f} seconds")
        
        print("=" * 35)
    
    def clear_snapshots(self):
        """Clear all snapshots"""
        self.snapshots.clear()


# Global performance monitor instance
performance_monitor = None

def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor instance"""
    global performance_monitor
    if performance_monitor is None:
        performance_monitor = PerformanceMonitor()
    return performance_monitor