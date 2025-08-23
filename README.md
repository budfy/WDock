# WDock - Windows Dock Application
# WDock - Застосунок Док-панелі для Windows

[English](#english) | [Українська](#українська)

---

## English

### 1. General Description

WDock is a modern, customizable dock panel for Windows with advanced features and smooth animations. Developed using Python and PyQt6, it provides a macOS-like dock experience for Windows users with intelligent positioning, auto-hide functionality, and comprehensive customization options.

**Key Highlights:**
- Modern PyQt6-based architecture with transparent, frameless windows
- CSS-like alignment behavior for intuitive positioning
- Dynamic theme support synchronized with Windows system themes
- Complete context menu system for all components
- Low memory footprint (optimized for <50MB usage)
- Bilingual interface (English/Ukrainian) with comprehensive documentation

### 2. Currently Implemented Features

#### ✅ Core Functionality (100% Complete)
- **Frameless Window System**: Transparent, always-on-top main window with proper Windows integration
- **Configuration Management**: JSON-based config system in `%APPDATA%\WDock\` with automatic persistence
- **Project Architecture**: Modular design with separated core logic, UI components, and utilities

#### ✅ Dock Features (100% Complete)
- **Multi-Position Support**: Attach to all 4 screen edges (top, bottom, left, right)
- **CSS-like Alignment**: Flexible positioning with start/center/end alignment (margin auto behavior)
- **Intelligent Auto-Hide**: Smart hiding with fullscreen application detection
- **Multi-Monitor Support**: Works seamlessly across multiple displays with DPI awareness

#### ✅ Icon Management (100% Complete)
- **Adaptive Icon System**: 48x48px icons with hover effects and smooth animations
- **Drag & Drop Support**: Add shortcuts (.lnk, .exe files) via drag and drop
- **Smart Grouping**: Drag-to-group functionality with popup expansion
- **Icon Extraction**: Native Windows icon extraction from executables and shortcuts

#### ✅ User Interface (100% Complete)
- **Comprehensive Context Menus**: Complete menus for dock, shortcuts, and groups with Lucide icons
- **Settings Window**: Full configuration interface with dynamic theme support
- **System Tray Integration**: Background operation with tray icon and comprehensive controls
- **About Dialog**: Application information and version display

#### ✅ Theme System (100% Complete)
- **Dynamic Theme Detection**: Automatic Windows registry-based theme detection
- **Theme Synchronization**: Dark/light themes synchronized with Windows system settings
- **Real-time Updates**: Instant theme switching without application restart
- **Configuration-aware Theming**: Respects user preference (auto/light/dark)

#### ✅ Context Menu System (100% Complete)
- **Dock Panel Context Menu**: Right-click on dock shows position, alignment, and behavior controls
- **Icon Context Menus**: Complete menus with open, rename, remove, properties, and dock controls
- **System Tray Integration**: Single-click tray icon shows dock context menu at cursor position
- **Lucide Icon Integration**: Consistent iconography across all menus

#### ✅ Performance & Integration (95% Complete)
- **Memory Optimization**: Efficient icon caching and low memory footprint
- **Windows Integration**: Registry-based startup management and system tray support
- **Animation System**: Smooth transitions using QPropertyAnimation
- **Error Handling**: Graceful fallbacks and comprehensive exception handling

### 3. Unimplemented Features

#### ⏳ Testing & Quality Assurance (30% Complete)
- **Comprehensive Unit Tests**: Expand test coverage beyond basic functionality
- **Integration Testing**: Full end-to-end testing scenarios
- **Performance Testing**: Memory usage and CPU utilization benchmarks
- **Multi-Monitor Testing**: Comprehensive testing across different display configurations

#### ⏳ Distribution & Deployment (60% Complete)
- **Windows Installer**: Professional MSI installer package
- **Portable Version**: Standalone ZIP distribution
- **Auto-Updater**: Automatic update checking and installation
- **Code Signing**: Digital certificate signing for Windows SmartScreen compatibility

#### ⏳ Advanced Features (Not Started)
- **Hotkey System**: Global keyboard shortcuts (e.g., Win+D for dock toggle)
- **Usage Analytics**: Application launch frequency tracking and statistics
- **Plugin Architecture**: Extensible plugin system for third-party enhancements
- **Custom Themes**: CSS-based theming system beyond light/dark modes
- **Animation Presets**: Multiple animation speed and style options
- **Backup/Sync**: Configuration backup and synchronization across devices

### 4. Known Bugs

#### ❌ Test Suite Issues
**Status**: Non-critical, development only
- **Configuration Persistence**: Tests fail due to existing configuration files from previous runs
- **PyQt6 Mock Compatibility**: QPainter mocking issues in `create_drag_pixmap` test
- **State Management**: Tests don't properly isolate configuration state

**Fix Requirements**:
- Implement temporary configuration files for tests
- Update PyQt6 mocking approach for better compatibility
- Add proper test state cleanup and isolation

#### ⚠️ Minor UI Issues
**Status**: Cosmetic, low priority
- **UpdateLayeredWindowIndirect Warnings**: Console warnings related to Windows graphics effects (does not affect functionality)
- **First Launch Theme Detection**: Rare cases where theme detection may fail on first application launch

**Fix Status**: Planned for next minor release

### 5. Build Instructions for EXE File

#### Prerequisites
```bash
# Ensure Python 3.8+ is installed
python --version

# Install dependencies
pip install -r requirements.txt

# Install build dependencies
pip install pyinstaller
```

#### Build Process
```bash
# Navigate to project directory
cd d:\WinDock

# Run automated build script
python build.py

# Or manual build (alternative)
pyinstaller --clean WDock.spec
```

#### Build Script Features
The `build.py` script automatically:
- **Installs PyInstaller** if not present
- **Creates Application Icon** using PIL if assets/wdock.ico doesn't exist
- **Generates PyInstaller Spec** with proper dependencies and configuration
- **Builds Executable** in `dist/WDock/` directory
- **Creates Portable ZIP** with documentation and required files
- **Includes All Dependencies**: PyQt6, pywin32, Pillow, etc.

#### Build Outputs
After successful build:
```
dist/
├── WDock/                    # Executable directory
│   ├── WDock.exe            # Main application
│   ├── src/                 # Source files
│   └── [PyQt6 dependencies] # Runtime libraries
└── WDock-1.0.0-Portable.zip # Portable distribution
```

#### Distribution Options

**Option 1: Portable Version**
- Extract `WDock-1.0.0-Portable.zip`
- Run `WDock.exe` directly
- No installation required

**Option 2: Manual Installation**
- Copy `dist/WDock/` folder to desired location
- Create desktop shortcut to `WDock.exe`
- Optionally add to Windows startup

#### Build Troubleshooting

**Common Issues:**
- **PyInstaller Import Errors**: Ensure all dependencies in requirements.txt are installed
- **Missing Icon**: Build script creates default icon if assets/wdock.ico is missing
- **Large File Size**: Normal - includes complete PyQt6 runtime (~80-100MB)
- **Antivirus Warnings**: Expected for unsigned executables - submit for whitelisting if needed

**Performance Tips:**
- Use `--onefile` flag for single executable (slower startup)
- Keep directory structure for faster loading
- Use UPX compression (enabled by default) for smaller file size

#### System Requirements
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100MB for application + dependencies
- **Display**: Any resolution, multi-monitor support included
- **.NET Framework**: 4.7.2 or higher (usually pre-installed)

#### Installation Verification
```bash
# Test the built executable
cd dist/WDock
WDock.exe

# Check version and dependencies
# (Application should start without errors)
```

---

## Українська

Сучасна, налаштовувана док-панель для Windows з розширеними функціями та плавними анімаціями.

### Можливості

- **Адаптивні Іконки**: Іконки 48x48px з ефектами наведення
- **Гнучке Позиціонування**: Прикріплення до будь-якого краю екрана (верх, низ, ліво, право)
- **Розумне Групування**: Перетягніть ярлики разом для створення груп
- **Інтелектуальне Автоприховування**: Автоматичне приховування під час повноекранних програм
- **Підтримка Тем**: Темна/світла теми синхронізовані з Windows
- **Плавні Анімації**: Плавна поява, приховування та розгортання груп
- **Підтримка Кількох Моніторів**: Бездоганна робота на кількох дисплеях
- **Низьке Використання Пам'яті**: Оптимізовано для використання менше 50МБ ОЗП
- **Інтеграція Системного Трею**: Робота ### 5. Інструкція для Збірки Проєкту в EXE-файл

```bash
# Переконайтеся, що встановлено Python 3.8+
python --version

# Встановіть залежності
pip install -r requirements.txt
pip install pyinstaller

# Запустіть автоматичну збірку
python build.py
```

**Вихідні Файли**: `dist/WDock/WDock.exe` та `WDock-1.0.0-Portable.zip`

**Системні Вимоги**: Windows 10/11 (64-біт), 4ГБ+ ОЗП, 100МБ місця