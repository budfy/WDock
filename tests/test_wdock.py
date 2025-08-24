"""
Unit Tests for WDock
Comprehensive test suite for all major components
"""

import unittest
import tempfile
import os
import sys
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.config_manager import ConfigManager
from src.utils.startup_manager import StartupManager
from src.utils.drag_drop import DragDropHelper


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_manager = ConfigManager()
        # Override config directory for testing
        self.config_manager.config_dir = Path(self.temp_dir)
        self.config_manager.config_file = self.config_manager.config_dir / 'config.json'
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_default_config(self):
        """Test default configuration values"""
        config = self.config_manager.load_config()
        
        self.assertEqual(config["position"], "bottom")
        self.assertEqual(config["alignment"], "center")
        self.assertTrue(config["auto_hide"])
        self.assertTrue(config["intelligent_hide"])
        self.assertTrue(config["always_on_top"])
        self.assertEqual(config["theme"], "auto")
        self.assertEqual(config["icon_size"], 48)
        self.assertEqual(config["animation_speed"], 200)
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration"""
        # Modify config
        self.config_manager.set("position", "top")
        self.config_manager.set("alignment", "left")
        
        # Create new config manager to test loading
        new_config_manager = ConfigManager()
        new_config_manager.config_dir = Path(self.temp_dir)
        new_config_manager.config_file = new_config_manager.config_dir / 'config.json'
        new_config = new_config_manager.load_config()
        
        self.assertEqual(new_config["position"], "top")
        self.assertEqual(new_config["alignment"], "left")
    
    def test_add_icon(self):
        """Test adding icons to configuration"""
        test_path = "C:\\test\\app.exe"
        test_name = "Test App"
        
        self.config_manager.add_icon(test_path, test_name)
        
        icons = self.config_manager.get_icons()
        self.assertEqual(len(icons), 1)
        self.assertEqual(icons[0]["path"], test_path)
        self.assertEqual(icons[0]["name"], test_name)
    
    def test_remove_icon(self):
        """Test removing icons from configuration"""
        test_path = "C:\\test\\app.exe"
        
        # Add icon first
        self.config_manager.add_icon(test_path, "Test App")
        self.assertEqual(len(self.config_manager.get_icons()), 1)
        
        # Remove icon
        self.config_manager.remove_icon(test_path)
        self.assertEqual(len(self.config_manager.get_icons()), 0)
    
    def test_add_group(self):
        """Test adding groups to configuration"""
        group_name = "Test Group"
        display_name = "Test Group Display"
        icon = "🎮"
        
        self.config_manager.add_group(group_name, display_name, icon)
        
        groups = self.config_manager.get_groups()
        self.assertIn(group_name, groups)
        self.assertEqual(groups[group_name]["name"], display_name)
        self.assertEqual(groups[group_name]["icon"], icon)
    
    def test_remove_group(self):
        """Test removing groups from configuration"""
        group_name = "Test Group"
        
        # Add group and icon
        self.config_manager.add_group(group_name)
        self.config_manager.add_icon("C:\\test\\app.exe", "Test App", group_name)
        
        # Verify setup
        self.assertIn(group_name, self.config_manager.get_groups())
        self.assertEqual(self.config_manager.get_icons()[0]["group"], group_name)
        
        # Remove group
        self.config_manager.remove_group(group_name)
        
        # Verify removal
        self.assertNotIn(group_name, self.config_manager.get_groups())
        self.assertIsNone(self.config_manager.get_icons()[0]["group"])


class TestStartupManager(unittest.TestCase):
    """Test cases for StartupManager"""
    
    def setUp(self):
        """Set up test environment"""
        self.startup_manager = StartupManager()
    
    def test_get_app_path(self):
        """Test getting application path"""
        app_path = self.startup_manager.get_app_path()
        self.assertIsInstance(app_path, str)
        self.assertTrue(len(app_path) > 0)
    
    @patch('winreg.OpenKey')
    @patch('winreg.QueryValueEx')
    def test_is_startup_enabled_true(self, mock_query, mock_open):
        """Test checking startup status when enabled"""
        mock_query.return_value = (self.startup_manager.app_path, None)
        
        result = self.startup_manager.is_startup_enabled()
        self.assertTrue(result)
    
    @patch('winreg.OpenKey')
    @patch('winreg.QueryValueEx')
    def test_is_startup_enabled_false(self, mock_query, mock_open):
        """Test checking startup status when disabled"""
        mock_query.side_effect = FileNotFoundError()
        
        result = self.startup_manager.is_startup_enabled()
        self.assertFalse(result)
    
    @patch('winreg.OpenKey')
    @patch('winreg.SetValueEx')
    def test_enable_startup(self, mock_set, mock_open):
        """Test enabling startup"""
        result = self.startup_manager.enable_startup()
        self.assertTrue(result)
        mock_set.assert_called_once()
    
    @patch('winreg.OpenKey')
    @patch('winreg.DeleteValue')
    def test_disable_startup(self, mock_delete, mock_open):
        """Test disabling startup"""
        result = self.startup_manager.disable_startup()
        self.assertTrue(result)
        mock_delete.assert_called_once()


class TestDragDropHelper(unittest.TestCase):
    """Test cases for DragDropHelper"""
    
    def test_create_drag_pixmap(self):
        """Test creating drag pixmap"""
        # Mock widget
        mock_widget = Mock()
        mock_widget.size.return_value = Mock()
        mock_widget.size.return_value.width.return_value = 64
        mock_widget.size.return_value.height.return_value = 64
        mock_widget.render = Mock()
        
        with patch('src.utils.drag_drop.QPixmap') as mock_pixmap:
            mock_pixmap_instance = Mock()
            mock_pixmap.return_value = mock_pixmap_instance
            
            result = DragDropHelper.create_drag_pixmap(mock_widget)
            
            mock_pixmap.assert_called_once()
            self.assertEqual(result, mock_pixmap_instance)
    
    def test_is_wdock_icon_drag(self):
        """Test detecting WDock icon drag"""
        # Mock mime data
        mock_mime_data = Mock()
        mock_mime_data.hasFormat.return_value = True
        
        result = DragDropHelper.is_wdock_icon_drag(mock_mime_data)
        self.assertTrue(result)
        mock_mime_data.hasFormat.assert_called_with("application/x-wdock-icon")
    
    def test_extract_icon_data(self):
        """Test extracting icon data from mime data"""
        test_data = {"path": "C:\\test\\app.exe", "name": "Test App"}
        json_data = json.dumps(test_data).encode()
        
        # Mock mime data
        mock_mime_data = Mock()
        mock_mime_data.hasFormat.return_value = True
        mock_data = Mock()
        mock_data.data.return_value.decode.return_value = json.dumps(test_data)
        mock_mime_data.data.return_value = mock_data
        
        result = DragDropHelper.extract_icon_data(mock_mime_data)
        self.assertEqual(result, test_data)
    
    def test_is_external_file_drag(self):
        """Test detecting external file drag"""
        mock_mime_data = Mock()
        mock_mime_data.hasUrls.return_value = True
        
        result = DragDropHelper.is_external_file_drag(mock_mime_data)
        self.assertTrue(result)
    
    def test_extract_file_paths(self):
        """Test extracting file paths from mime data"""
        # Mock URL objects
        mock_url1 = Mock()
        mock_url1.toLocalFile.return_value = "C:\\test\\app.exe"
        mock_url2 = Mock()
        mock_url2.toLocalFile.return_value = "C:\\test\\shortcut.lnk"
        mock_url3 = Mock()
        mock_url3.toLocalFile.return_value = "C:\\test\\document.txt"  # Should be filtered out
        
        mock_mime_data = Mock()
        mock_mime_data.hasUrls.return_value = True
        mock_mime_data.urls.return_value = [mock_url1, mock_url2, mock_url3]
        
        result = DragDropHelper.extract_file_paths(mock_mime_data)
        
        expected = ["C:\\test\\app.exe", "C:\\test\\shortcut.lnk"]
        self.assertEqual(result, expected)


class TestIntegration(unittest.TestCase):
    """Integration tests for WDock components"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_manager = ConfigManager()
        self.config_manager.config_dir = Path(self.temp_dir)
        self.config_manager.config_file = self.config_manager.config_dir / 'config.json'
    
    def tearDown(self):
        """Clean up integration test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_icon_group_workflow(self):
        """Test complete icon and group workflow"""
        # Add icons
        self.config_manager.add_icon("C:\\test\\app1.exe", "App 1")
        self.config_manager.add_icon("C:\\test\\app2.exe", "App 2")
        
        # Verify icons added
        icons = self.config_manager.get_icons()
        self.assertEqual(len(icons), 2)
        
        # Create group
        self.config_manager.add_group("TestGroup", "Test Group", "🎮")
        
        # Assign icons to group
        for icon in self.config_manager.config["icons"]:
            icon["group"] = "TestGroup"
        self.config_manager.save_config()
        
        # Reload and verify
        new_config = self.config_manager.load_config()
        for icon in new_config["icons"]:
            self.assertEqual(icon["group"], "TestGroup")
        
        # Remove group
        self.config_manager.remove_group("TestGroup")
        
        # Verify icons are ungrouped
        icons = self.config_manager.get_icons()
        for icon in icons:
            self.assertIsNone(icon["group"])
    
    def test_config_persistence(self):
        """Test configuration persistence across restarts"""
        # Set various config values
        settings = {
            "position": "right",
            "alignment": "end",
            "auto_hide": False,
            "theme": "dark",
            "icon_size": 56,
            "animation_speed": 300
        }
        
        for key, value in settings.items():
            self.config_manager.set(key, value)
        
        # Add some icons and groups
        self.config_manager.add_icon("C:\\test\\app1.exe", "App 1")
        self.config_manager.add_group("Games", "Game Applications", "🎮")
        
        # Create new config manager (simulating restart)
        new_config_manager = ConfigManager()
        new_config_manager.config_dir = Path(self.temp_dir)
        new_config_manager.config_file = new_config_manager.config_dir / 'config.json'
        new_config = new_config_manager.load_config()
        
        # Verify all settings persisted
        for key, value in settings.items():
            self.assertEqual(new_config[key], value)
        
        # Verify icons and groups persisted
        self.assertEqual(len(new_config_manager.get_icons()), 1)
        self.assertIn("Games", new_config_manager.get_groups())


def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_cases = [
        TestConfigManager,
        TestStartupManager,
        TestDragDropHelper,
        TestIntegration
    ]
    
    for test_case in test_cases:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_case)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=== WDock Unit Tests ===")
    success = run_tests()
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)