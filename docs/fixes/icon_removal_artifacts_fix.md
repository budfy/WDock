# Fix: Icon Removal Artifacts

## Problem
After deleting shortcuts from the dock, visual artifacts of the deleted shortcuts remained visible. This was causing the dock to display remnants of removed icons.

## Root Cause
The `remove_from_dock()` method in `IconWidget` was incomplete and marked with a TODO comment. It only called:
```python
self.setParent(None)
self.deleteLater()
```

This approach failed to:
1. Remove the icon from the configuration file
2. Remove the widget from the dock layout properly  
3. Update the dock size after removal
4. Trigger proper cleanup and refresh

## Solution
Modified the `remove_from_dock()` method in `src/ui/icon_widget.py` to properly delegate to the dock window's complete removal process:

```python
def remove_from_dock(self):
    """Remove this icon from the dock"""
    from PyQt6.QtWidgets import QMessageBox
    
    reply = QMessageBox.question(
        self, "Видалення", 
        f"Видалити '{self.icon_data.get('name', 'цей ярлик')}' з доку?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    
    if reply == QMessageBox.StandardButton.Yes:
        # Get parent dock window and delegate proper removal
        dock_window = self.get_dock_window()
        if dock_window:
            # Use the dock window's proper removal method
            # This handles config removal, layout cleanup, and dock size update
            dock_window.remove_icon_widget(self)
        else:
            # Fallback if dock window not found
            self.setParent(None)
            self.deleteLater()
```

## What the Fix Does
The fix ensures that when an icon is removed, the `DockWindow.remove_icon_widget()` method is called, which properly:

1. **Removes from configuration**: `self.config_manager.remove_icon(icon_path)`
2. **Removes from layout**: `self.dock_layout.removeWidget(icon_widget)`  
3. **Deletes the widget**: `icon_widget.deleteLater()`
4. **Updates dock size**: `self.update_dock_size()`

## Testing
To test the fix:
1. Run WDock
2. Right-click on any icon in the dock
3. Select "Видалити з доку" (Remove from dock)
4. Confirm the deletion
5. Verify that:
   - The icon disappears completely
   - No visual artifacts remain
   - The dock properly resizes
   - The icon is removed from the config file

## Files Modified
- `src/ui/icon_widget.py`: Fixed the `remove_from_dock()` method

## Related Methods
- `DockWindow.remove_icon_widget()`: The proper removal implementation
- `ConfigManager.remove_icon()`: Configuration cleanup
- `DockWindow.update_dock_size()`: Size recalculation after removal