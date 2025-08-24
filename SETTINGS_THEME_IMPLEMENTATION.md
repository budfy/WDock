# Settings Window Theme Implementation

## Issue Fixed

**Problem**: The settings window had a white background with white/light text, making it unreadable. The settings window theme did not follow the operating system theme, and text and icons lacked proper contrast against the background.

**Solution**: Implemented dynamic theme detection and applied appropriate light/dark theme styles based on the system theme and user configuration.

## Implementation Details

### Theme Detection

The settings window now includes:
- **System Theme Detection**: Uses Windows registry to detect if the system is using dark or light theme
- **Configuration Respect**: Honors the user's theme preference setting (auto/light/dark)
- **Dynamic Updates**: Theme changes apply immediately when settings are modified

### Key Methods Added

#### 1. `is_dark_theme()` - System Theme Detection
```python
def is_dark_theme(self) -> bool:
    """Detect if Windows is using dark theme"""
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return value == 0  # 0 = dark theme, 1 = light theme
    except:
        return False  # Default to light theme
```

#### 2. `get_current_theme_is_dark()` - Configuration-Aware Theme Detection
```python
def get_current_theme_is_dark(self) -> bool:
    """Get whether current theme should be dark based on configuration"""
    theme = self.config_manager.get("theme", "auto")
    if theme == "auto":
        return self.is_dark_theme()
    else:
        return theme == "dark"
```

#### 3. `apply_light_theme()` and `apply_dark_theme()` - Theme-Specific Styling
- Complete styling for all UI components
- Proper contrast between text and background
- Theme-appropriate colors for buttons, checkboxes, radio buttons, etc.

### Visual Improvements

#### Light Theme Features:
- **Background**: Light gray (#F5F5F5) with white content areas
- **Text**: Black (#000000) for maximum contrast
- **Controls**: Light gray backgrounds with proper border colors
- **Buttons**: Standard light button styling with blue accent for default buttons

#### Dark Theme Features:
- **Background**: Dark gray (#2B2B2B) with darker content areas
- **Text**: White (#FFFFFF) for maximum contrast
- **Controls**: Dark backgrounds (#3C3C3C) with lighter borders
- **Buttons**: Dark button styling with same blue accent system

### Component Styling Coverage

All UI components are properly themed:
- ✅ **Dialog Background**: Theme-appropriate base color
- ✅ **Tab Widget**: Proper tab styling with theme colors
- ✅ **Group Boxes**: Contrasting borders and title backgrounds
- ✅ **Labels**: Correct text colors for readability
- ✅ **Buttons**: Theme-appropriate backgrounds and hover effects
- ✅ **Checkboxes**: Proper indicator colors and backgrounds
- ✅ **Radio Buttons**: Theme-appropriate styling
- ✅ **Input Fields**: Text boxes with proper backgrounds and text colors
- ✅ **Sliders**: Theme-appropriate groove and handle colors
- ✅ **Text Areas**: Proper background and text contrast

### Dynamic Theme Updates

The implementation includes:
- **Real-time Updates**: Theme changes when user modifies theme settings
- **Icon Updates**: Tab icons update to match theme (light/dark variants)
- **Immediate Application**: Changes apply without restart requirement

### Integration Points

#### 1. Settings Window Creation
- Theme detection occurs during initialization
- Proper theme applied based on current configuration

#### 2. Settings Changes
- Theme reapplied when user changes theme preference
- Icons updated to match new theme
- Visual feedback is immediate

#### 3. Context Menu Integration
- Settings window opened from dock context menu uses proper theme
- Consistent with overall application theming

## Usage

### Automatic Theme Detection
- When theme is set to "auto", the window automatically detects Windows theme
- Dark system theme → Dark settings window
- Light system theme → Light settings window

### Manual Theme Control
- User can explicitly choose "Light" or "Dark" theme
- Settings window immediately reflects the choice
- Theme persists across application restarts

### Theme Change Workflow
1. User opens settings window
2. Current theme is detected/applied
3. User changes theme preference
4. Theme immediately updates with new styling
5. Icons and all UI elements refresh

## Technical Notes

### Registry Integration
- Uses Windows registry path: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize`
- Reads `AppsUseLightTheme` value (0 = dark, 1 = light)
- Graceful fallback to light theme if registry access fails

### Performance Considerations
- Theme detection is lightweight (single registry read)
- Styling applied via Qt StyleSheets for optimal performance
- Theme changes are efficient (no window recreation needed)

### Compatibility
- Works with Windows 10 and Windows 11 theme systems
- Compatible with system-wide dark mode settings
- Supports all Windows theme variants

## Testing Verification

The implementation has been tested and verified:
- ✅ Auto theme detection works correctly
- ✅ Manual theme switching functions properly
- ✅ All UI components have proper contrast
- ✅ Text is readable in both light and dark themes
- ✅ Icons update correctly with theme changes
- ✅ Settings persist across application restarts

The settings window now provides a consistent, accessible interface that respects user preferences and system theme settings.