# Fix: Icon and Group Removal Artifacts

## Problem
After deleting shortcuts or groups from the dock, visual artifacts of the deleted items remained visible. This was causing the dock to display remnants of removed icons and groups.

## Root Cause
Multiple incomplete removal methods were marked with TODO comments and only performed partial cleanup:

1. **IconWidget.remove_from_dock()**: Only called `self.setParent(None)` and `self.deleteLater()`
2. **GroupWidget.ungroup()**: Had TODO comment with `pass` statement
3. **GroupWidget.delete_group()**: Only called `self.setParent(None)` and `self.deleteLater()`

These approaches failed to:
1. Remove items from the configuration file
2. Remove widgets from the dock layout properly  
3. Update the dock size after removal
4. Trigger proper cleanup and refresh

## Solution
Implemented complete removal workflows for both icons and groups:

### Icon Removal Fix
Modified `IconWidget.remove_from_dock()` in `src/ui/icon_widget.py` to properly delegate to the dock window:

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
            dock_window.remove_icon_widget(self)
        else:
            # Fallback if dock window not found
            self.setParent(None)
            self.deleteLater()
```

### Group Removal Fixes
Added proper group removal methods to `DockWindow` in `src/core/dock_window.py`:

```python
def remove_group_widget(self, group_widget):
    """Remove a group widget from the dock (ungroup)"""
    # Find the group name by matching group data
    group_name = None
    for name, data in self.config_manager.get_groups().items():
        if data == group_widget.group_data:
            group_name = name
            break
    
    if group_name:
        # Remove the group (this ungroups all icons in the group)
        self.config_manager.remove_group(group_name)
    
    # Remove widget from layout and reload to show ungrouped icons
    if hasattr(self, 'dock_layout'):
        self.dock_layout.removeWidget(group_widget)
    group_widget.deleteLater()
    self.load_icons()

def delete_group_widget(self, group_widget):
    """Delete a group widget and all its icons from the dock"""
    # Find group name and remove all icons in the group
    group_name = None
    for name, data in self.config_manager.get_groups().items():
        if data == group_widget.group_data:
            group_name = name
            break
    
    if group_name:
        # Remove all icons that belong to this group
        icons_to_remove = [icon["path"] for icon in self.config_manager.get_icons() 
                          if icon.get("group") == group_name]
        
        for icon_path in icons_to_remove:
            self.config_manager.remove_icon(icon_path)
        
        # Remove the group itself
        del self.config_manager.config["groups"][group_name]
        self.config_manager.save_config()
    
    # Remove widget from layout and reload
    if hasattr(self, 'dock_layout'):
        self.dock_layout.removeWidget(group_widget)
    group_widget.deleteLater()
    self.load_icons()
```

Fixed `GroupWidget` methods in `src/ui/group_widget.py` to delegate properly:

```python
def ungroup(self):
    """Ungroup the items (break up the group)"""
    # ... confirmation dialog ...
    if reply == QMessageBox.StandardButton.Yes:
        dock_window = self.get_dock_window()
        if dock_window:
            dock_window.remove_group_widget(self)
        else:
            self.setParent(None)
            self.deleteLater()

def delete_group(self):
    """Delete the entire group"""
    # ... confirmation dialog ...
    if reply == QMessageBox.StandardButton.Yes:
        dock_window = self.get_dock_window()
        if dock_window:
            dock_window.delete_group_widget(self)
        else:
            self.setParent(None)
            self.deleteLater()
```

## What the Fix Does
The complete fix ensures that when icons or groups are removed:

### Icon Removal:
1. **Removes from configuration**: `self.config_manager.remove_icon(icon_path)`
2. **Removes from layout**: `self.dock_layout.removeWidget(icon_widget)`  
3. **Deletes the widget**: `icon_widget.deleteLater()`
4. **Updates dock size**: `self.update_dock_size()`

### Group Ungrouping:
1. **Removes group from configuration**: `self.config_manager.remove_group(group_name)` (sets icon group to None)
2. **Removes widget from layout**: `self.dock_layout.removeWidget(group_widget)`
3. **Deletes the widget**: `group_widget.deleteLater()`
4. **Reloads icons**: `self.load_icons()` (shows ungrouped icons individually)

### Group Deletion:
1. **Removes all group icons**: Removes each icon's configuration entry
2. **Removes group configuration**: Deletes the group data
3. **Removes widget from layout**: `self.dock_layout.removeWidget(group_widget)`
4. **Deletes the widget**: `group_widget.deleteLater()`
5. **Reloads dock**: `self.load_icons()` (updates display and dock size)

## Testing
To test the fixes:

### Icon Removal:
1. Run WDock
2. Right-click on any icon
3. Select "Видалити з доку" (Remove from dock)
4. Confirm deletion
5. Verify: icon disappears, no artifacts, dock resizes properly

### Group Operations:
1. Create a group by dragging one icon onto another
2. Right-click on the group
3. Test "Розгрупувати" (Ungroup): Group becomes individual icons
4. Test "Видалити групу" (Delete group): Entire group and all icons removed
5. Verify: no artifacts, proper cleanup, dock resizes correctly

## Files Modified
- `src/ui/icon_widget.py`: Fixed `remove_from_dock()` method
- `src/ui/group_widget.py`: Fixed `ungroup()` and `delete_group()` methods, added `get_dock_window()`
- `src/core/dock_window.py`: Added `remove_group_widget()` and `delete_group_widget()` methods

## Related Methods
- `DockWindow.remove_icon_widget()`: Proper icon removal implementation
- `DockWindow.remove_group_widget()`: Proper group ungrouping implementation  
- `DockWindow.delete_group_widget()`: Proper group deletion implementation
- `ConfigManager.remove_icon()`: Configuration cleanup for icons
- `ConfigManager.remove_group()`: Configuration cleanup for groups
- `DockWindow.update_dock_size()`: Size recalculation after removal
- `DockWindow.load_icons()`: Full dock refresh and layout rebuild