# Fix: Rendering Issues and Widget Deletion Errors

## Problem
The application was experiencing two main issues:
1. **UpdateLayeredWindowIndirect errors**: These were appearing in the console output, indicating problems with the shadow effects
2. **RuntimeError: wrapped C/C++ object has been deleted**: This error occurred when trying to emit signals or access widget properties after the widget had been deleted

## Root Cause
1. **Shadow Effect Issues**: The `QGraphicsDropShadowEffect` with large blur radius values was causing coordinate translation issues with the Windows layered window system
2. **Widget Lifecycle Management**: Signal emissions and animation callbacks were not properly checking if the widget was still valid before accessing its properties

## Solution

### Shadow Effect Fix
Reduced blur radius values in all shadow effects to prevent positioning issues:

```python
# Before (in dock_window.py)
shadow.setBlurRadius(20)  # Caused positioning issues
shadow.setYOffset(2)

# After (in dock_window.py)  
shadow.setBlurRadius(10)  # Reduced to prevent issues
shadow.setYOffset(1)      # Also reduced

# Before (in group_widget.py)
shadow.setBlurRadius(20)
shadow.setYOffset(4)

# After (in group_widget.py)
shadow.setBlurRadius(8)   # Reduced from 20 to prevent positioning issues
shadow.setYOffset(2)      # Reduced from 4
```

### Widget Deletion Fix
Added proper error handling to prevent accessing deleted widgets:

1. **Mouse Event Handlers**: Added try/except blocks and validity checks
```python
def mouseReleaseEvent(self, event):
    try:
        # ... event handling code ...
        if not self.parent() is None:  # Check widget validity
            self.clicked.emit()
    except RuntimeError:
        # Widget has been deleted, ignore the event
        pass
```

2. **Timer Callbacks**: Added try/except blocks for delayed operations
```python
def check_close_popup(self):
    try:
        if self.is_expanded and self.popup_widget:
            # Check if mouse is over popup or group
            if not (self.underMouse() or self.popup_widget.underMouse()):
                self.collapse_group()
    except RuntimeError:
        # Widget has been deleted, ignore the event
        pass
```

3. **Animation Callbacks**: Added try/except blocks for animation finished handlers
```python
def return_to_normal():
    try:
        self.bounce_animation.setStartValue(bounce_geo)
        self.bounce_animation.setEndValue(current_geo)
        self.bounce_animation.finished.disconnect()
        self.bounce_animation.start()
    except RuntimeError:
        # Widget has been deleted, ignore the callback
        pass
```

## Files Modified
- `src/ui/icon_widget.py`: Fixed mouse event handlers, animation callbacks
- `src/ui/group_widget.py`: Fixed mouse event handlers, shadow effects, timer callbacks

## Testing
To test the fixes:
1. Run WDock and observe console output - UpdateLayeredWindowIndirect errors should be significantly reduced
2. Add/remove icons and groups rapidly to test widget deletion scenarios
3. Right-click icons and groups to verify context menus work properly
4. Verify that no RuntimeError exceptions occur during normal usage

## Related Memory
This fix addresses the known issue from the memory about PyQt6 Windows GUI rendering issues where large blur radius values can cause coordinate translation issues with the layered window system.